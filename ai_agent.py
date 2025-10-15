import openai
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import config
from calendar_manager import CalendarManager

class ScheduleAIAgent:
    def __init__(self):
        if config.OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        else:
            self.client = None
        self.calendar_manager = CalendarManager()
        
    def analyze_schedule_request(self, user_request: str, duration_hours: float = 2.0) -> Dict:
        """Analyze user's schedule request and recommend optimal time"""
        
        # Get calendar data (next 2 weeks)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=14)
        
        events = self.calendar_manager.get_events(start_date, end_date)
        free_slots = self.calendar_manager.get_free_time_slots(
            start_date, end_date, int(duration_hours * 60)
        )
        
        # Request analysis from AI
        analysis = self._get_ai_analysis(user_request, events, free_slots, duration_hours)
        
        return {
            'user_request': user_request,
            'duration_hours': duration_hours,
            'analysis': analysis,
            'available_slots': free_slots,
            'current_events': events
        }
    
    def _get_ai_analysis(self, user_request: str, events: List[Dict], 
                        free_slots: List[Dict], duration_hours: float) -> Dict:
        """Schedule analysis and recommendation using OpenAI API"""
        
        if not self.client:
            return self._create_fallback_analysis(user_request, free_slots)
        
        # Convert event information to string
        events_summary = self._format_events_for_ai(events)
        slots_summary = self._format_slots_for_ai(free_slots)
        
        prompt = f"""
You are a professional schedule management AI assistant. Please analyze the user's request and recommend the optimal time.

User request: "{user_request}"
Required time: {duration_hours} hours

Current schedule:
{events_summary}

Available time slots:
{slots_summary}

Please provide the following information in JSON format:
1. Request analysis (what the user wants)
2. Optimal time recommendations (top 3 options)
3. Recommendation reasons
4. Precautions or tips

JSON format:
{{
    "request_analysis": "Analysis of user request",
    "recommendations": [
        {{
            "datetime": "YYYY-MM-DD HH:MM",
            "reason": "Recommendation reason",
            "priority": 1
        }}
    ],
    "general_advice": "General advice",
    "notes": "Precautions"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional schedule management AI assistant. Always respond in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            # Try JSON parsing
            try:
                return json.loads(ai_response)
            except json.JSONDecodeError:
                # Default response when JSON parsing fails
                return self._create_fallback_analysis(user_request, free_slots)
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._create_fallback_analysis(user_request, free_slots)
    
    def _format_events_for_ai(self, events: List[Dict]) -> str:
        """Convert event information to AI-friendly format"""
        if not events:
            return "No scheduled events currently."
        
        formatted = []
        for event in events[:10]:  # Only recent 10 events
            start_time = event['start'].strftime("%m/%d %H:%M")
            title = event['title']
            duration = int((event['end'] - event['start']).total_seconds() / 60)
            formatted.append(f"- {start_time}: {title} ({duration} min)")
        
        return "\n".join(formatted)
    
    def _format_slots_for_ai(self, slots: List[Dict]) -> str:
        """Convert available time slots to AI-friendly format"""
        if not slots:
            return "No available time slots."
        
        formatted = []
        for slot in slots[:15]:  # Only top 15 slots
            start_time = slot['start'].strftime("%m/%d %H:%M")
            duration = slot['duration_minutes']
            formatted.append(f"- {start_time}: {duration} min available")
        
        return "\n".join(formatted)
    
    def _create_fallback_analysis(self, user_request: str, free_slots: List[Dict]) -> Dict:
        """Provide basic analysis when AI API fails"""
        recommendations = []
        
        for i, slot in enumerate(free_slots[:3]):
            recommendations.append({
                "datetime": slot['start'].strftime("%Y-%m-%d %H:%M"),
                "reason": f"Sufficient time ({slot['duration_minutes']} min) is secured for this time slot.",
                "priority": i + 1
            })
        
        return {
            "request_analysis": f"Schedule analysis for '{user_request}'",
            "recommendations": recommendations,
            "general_advice": "Choose the most convenient time from the recommended time slots.",
            "notes": "AI analysis is temporarily unavailable, providing basic recommendations."
        }
    
    def get_smart_suggestions(self, user_request: str, duration_hours: float = 2.0) -> Dict:
        """More intelligent schedule suggestions (considering time slots, days, patterns)"""
        
        analysis = self.analyze_schedule_request(user_request, duration_hours)
        
        # Additional smart analysis
        smart_analysis = self._enhance_with_smart_analysis(
            user_request, analysis['available_slots']
        )
        
        analysis['smart_analysis'] = smart_analysis
        
        return analysis
    
    def _enhance_with_smart_analysis(self, user_request: str, slots: List[Dict]) -> Dict:
        """Enhance recommendations with smart analysis"""
        
        # Analyze optimal time slots by request type
        request_type = self._classify_request_type(user_request)
        
        # Calculate scores by time slot
        scored_slots = []
        for slot in slots:
            score = self._calculate_time_score(slot, request_type)
            scored_slots.append({
                **slot,
                'score': score,
                'reason': self._get_time_reason(slot, request_type)
            })
        
        # Sort by score
        scored_slots.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'request_type': request_type,
            'scored_slots': scored_slots[:5],
            'best_time_pattern': self._get_best_time_pattern(request_type)
        }
    
    def _classify_request_type(self, request: str) -> str:
        """Classify request type"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['hospital', 'doctor', 'checkup', 'dental', 'appointment']):
            return 'medical'
        elif any(word in request_lower for word in ['meeting', 'conference', 'presentation', 'present']):
            return 'business'
        elif any(word in request_lower for word in ['exercise', 'gym', 'yoga', 'fitness']):
            return 'fitness'
        elif any(word in request_lower for word in ['meal', 'lunch', 'dinner', 'cafe']):
            return 'social'
        elif any(word in request_lower for word in ['shopping', 'purchase', 'market']):
            return 'shopping'
        else:
            return 'general'
    
    def _calculate_time_score(self, slot: Dict, request_type: str) -> int:
        """Calculate scores by time slot"""
        hour = slot['start'].hour
        weekday = slot['start'].weekday()
        score = 50  # Base score
        
        # Optimal time slots by request type
        if request_type == 'medical':
            if 9 <= hour <= 11:  # Morning time slot
                score += 30
            elif 14 <= hour <= 16:  # Afternoon time slot
                score += 20
        elif request_type == 'business':
            if 9 <= hour <= 17:  # Business hours
                score += 25
        elif request_type == 'fitness':
            if 6 <= hour <= 8 or 18 <= hour <= 20:  # Exercise time slot
                score += 30
        elif request_type == 'social':
            if 12 <= hour <= 13 or 18 <= hour <= 20:  # Meal time slot
                score += 25
        elif request_type == 'shopping':
            if 10 <= hour <= 12 or 14 <= hour <= 16:  # Shopping time slot
                score += 20
        
        # Score by day of week
        if weekday < 5:  # Weekday
            score += 10
        elif weekday == 5:  # Saturday
            score += 5
        
        # Score by time length
        if slot['duration_minutes'] >= 120:  # 2 hours or more
            score += 15
        elif slot['duration_minutes'] >= 90:  # 1.5 hours or more
            score += 10
        
        return min(score, 100)  # Maximum 100 points
    
    def _get_time_reason(self, slot: Dict, request_type: str) -> str:
        """Reason for time slot selection"""
        hour = slot['start'].hour
        weekday = slot['start'].weekday()
        
        reasons = []
        
        if request_type == 'medical':
            if 9 <= hour <= 11:
                reasons.append("Morning time slots are less crowded at hospitals with shorter wait times")
            elif 14 <= hour <= 16:
                reasons.append("Afternoon time slots are convenient after lunch time")
        
        if weekday < 5:
            reasons.append("Weekdays have minimal impact on work")
        elif weekday == 5:
            reasons.append("Saturday allows for weekend utilization")
        
        if slot['duration_minutes'] >= 120:
            reasons.append("Sufficient time is secured to proceed comfortably")
        
        return "; ".join(reasons) if reasons else "Appropriate time slot"
    
    def _get_best_time_pattern(self, request_type: str) -> str:
        """Optimal time pattern by request type"""
        patterns = {
            'medical': "9-11 AM or 2-4 PM are most suitable",
            'business': "Weekday business hours 9 AM-5 PM are good",
            'fitness': "6-8 AM or 6-8 PM exercise time is suitable",
            'social': "Lunch time (12-1 PM) or evening time (6-8 PM) are good",
            'shopping': "10 AM-12 PM or 2-4 PM are suitable",
            'general': "Choose a time that fits your personal schedule"
        }
        
        return patterns.get(request_type, "Choose a time that fits your personal schedule")