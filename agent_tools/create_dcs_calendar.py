"""
DCS Calendar MCP Tool for SmolAgent integration
"""

import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from smolagents import Tool


class CreateDCSCalendarTool(Tool):
    """DCS Calendar tool that generates Slack template with actual dates"""
    
    name = "create_dcs_calendar"
    description = """A tool that creates DCS calendar Slack message template with actual working day dates.
    Takes a month input and generates the template with placeholder dates replaced by actual working days,
    excluding weekends and Norwegian public holidays."""
    
    inputs = {
        "month": {
            "type": "string",
            "description": "Month for the calendar (e.g., 'October', 'November', 'October 2025', '2025-10')"
        }
    }
    output_type = "string"
    
    def __init__(self):
        super().__init__()
        # Cache for holidays by year
        self.holidays_cache = {}
    
    def _get_norwegian_holidays(self, year: int) -> Dict[str, str]:
        """
        Fetch Norwegian public holidays for the given year from the API.
        
        Args:
            year: The year to fetch holidays for
            
        Returns:
            Dictionary with date strings as keys and holiday names as values
        """
        # Check cache first
        if year in self.holidays_cache:
            return self.holidays_cache[year]
            
        try:
            url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/NO"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            holidays_data = response.json()
            holidays_dict = {}
            
            for holiday in holidays_data:
                date_str = holiday['date']  # Already in YYYY-MM-DD format
                name = holiday['name']
                holidays_dict[date_str] = name
            
            # Cache the result
            self.holidays_cache[year] = holidays_dict
            return holidays_dict
            
        except Exception as e:
            print(f"Warning: Could not fetch Norwegian holidays for {year}: {e}")
            # Fallback to common Norwegian holidays
            fallback_holidays = {
                f"{year}-01-01": "New Year's Day",
                f"{year}-04-17": "Maundy Thursday", 
                f"{year}-04-18": "Good Friday",
                f"{year}-04-21": "Easter Monday",
                f"{year}-05-01": "Labour Day",
                f"{year}-05-17": "Constitution Day",
                f"{year}-05-29": "Ascension Day",
                f"{year}-06-09": "Whit Monday",
                f"{year}-12-25": "Christmas Day",
                f"{year}-12-26": "Boxing Day"
            }
            # Cache the fallback
            self.holidays_cache[year] = fallback_holidays
            return fallback_holidays
    
    def forward(self, month: str) -> str:
        """Generate DCS calendar template with actual dates"""
        try:
            # Parse the month input
            target_date = self._parse_month_input(month)
            if not target_date:
                return f"Error: Could not parse month '{month}'. Please use format like 'October', 'October 2025', or '2025-10'"
            
            # Load DCS calendar configuration
            calendar_config = self._load_dcs_calendar_config()
            if not calendar_config:
                return "Error: Could not load DCS calendar configuration"
            
            # Load Slack template
            template_config = self._load_slack_template_config()
            if not template_config:
                return "Error: Could not load Slack template configuration"
            
            # Calculate working day dates
            working_day_dates = self._calculate_working_day_dates(target_date, calendar_config)
            
            # Generate the template with actual dates
            template_text = self._generate_template_with_dates(template_config, working_day_dates)
            
            return template_text
            
        except Exception as e:
            return f"Error generating DCS calendar: {str(e)}"
    
    def _parse_month_input(self, month: str) -> Optional[datetime]:
        """Parse various month input formats"""
        try:
            current_year = datetime.now().year
            
            # Try different formats
            month_lower = month.lower().strip()
            
            # Format: "October 2025" or "October"
            if month_lower in ['january', 'february', 'march', 'april', 'may', 'june',
                             'july', 'august', 'september', 'october', 'november', 'december']:
                month_num = {
                    'january': 1, 'february': 2, 'march': 3, 'april': 4,
                    'may': 5, 'june': 6, 'july': 7, 'august': 8,
                    'september': 9, 'october': 10, 'november': 11, 'december': 12
                }[month_lower]
                return datetime(current_year, month_num, 1)
            
            # Format: "October 2025"
            parts = month.split()
            if len(parts) == 2:
                month_name = parts[0].lower()
                year = int(parts[1])
                if month_name in ['january', 'february', 'march', 'april', 'may', 'june',
                                'july', 'august', 'september', 'october', 'november', 'december']:
                    month_num = {
                        'january': 1, 'february': 2, 'march': 3, 'april': 4,
                        'may': 5, 'june': 6, 'july': 7, 'august': 8,
                        'september': 9, 'october': 10, 'november': 11, 'december': 12
                    }[month_name]
                    return datetime(year, month_num, 1)
            
            # Format: "2025-10"
            if '-' in month:
                year, month_num = month.split('-')
                return datetime(int(year), int(month_num), 1)
            
            return None
            
        except Exception:
            return None
    
    def _load_dcs_calendar_config(self) -> Optional[Dict]:
        """Load DCS calendar configuration"""
        try:
            config_path = "config/dcs_calendar.json"
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    
    def _load_slack_template_config(self) -> Optional[Dict]:
        """Load Slack template configuration"""
        try:
            config_path = "config/share_dcs_calendar_slack_template.json"
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    
    def _is_working_day(self, date: datetime) -> bool:
        """Check if a date is a working day (not weekend or Norwegian holiday)"""
        # Check if weekend (Saturday = 5, Sunday = 6)
        if date.weekday() >= 5:
            return False
        
        # Check if Norwegian holiday
        date_str = date.strftime("%Y-%m-%d")
        year = date.year
        holidays = self._get_norwegian_holidays(year)
        if date_str in holidays:
            return False
        
        return True
    
    def _calculate_working_day_dates(self, start_date: datetime, calendar_config: Dict) -> Dict[int, str]:
        """Calculate actual dates for each working day"""
        working_day_dates = {}
        current_date = start_date
        working_day_count = 0
        
        # Get the maximum working day needed
        max_working_day = 0
        for step in calendar_config["dcs_calendar"]["process_steps"]:
            working_day = int(step["number_working_day_due_date"])
            max_working_day = max(max_working_day, working_day)
        
        # Calculate dates for each working day
        while working_day_count < max_working_day:
            if self._is_working_day(current_date):
                working_day_count += 1
                working_day_dates[working_day_count] = self._format_date(current_date)
            current_date += timedelta(days=1)
        
        return working_day_dates
    
    def _format_date(self, date: datetime) -> str:
        """Format date as 'Tuesday, 2nd October'"""
        day_name = date.strftime("%A")
        day = date.day
        month_name = date.strftime("%B")
        
        # Add ordinal suffix
        if 10 <= day % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        
        return f"{day_name}, {day}{suffix} {month_name}"
    
    def _generate_template_with_dates(self, template_config: Dict, working_day_dates: Dict[int, str]) -> str:
        """Generate the template text with actual dates"""
        # Get the template array
        template_lines = template_config["share_dsc_calendar_slack_template"]["template"]
        
        # Join the template lines
        template_text = "\n".join(template_lines)
        
        # Load DCS calendar to get the actual working day mapping
        calendar_config = self._load_dcs_calendar_config()
        step_to_working_day = {}
        if calendar_config:
            for step in calendar_config["dcs_calendar"]["process_steps"]:
                step_num = step["step_number"]
                working_day = int(step["number_working_day_due_date"])
                step_to_working_day[step_num] = working_day
        
        # Replace placeholders with actual dates
        for i in range(1, 7):  # Steps 1-6
            placeholder = f"{{PLACEHOLDER_STEP_{i}_DATE}}"
            working_day = step_to_working_day.get(i, i)  # Default to step number if not found
            actual_date = working_day_dates.get(working_day, f"Working day {working_day}")
            template_text = template_text.replace(placeholder, actual_date)
        
        return template_text
