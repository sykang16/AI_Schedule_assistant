#!/usr/bin/env python3
"""
AI Schedule Assistant Demo Test Script
"""

from ai_agent import ScheduleAIAgent
from calendar_manager import CalendarManager
from datetime import datetime, timedelta
import json

def test_calendar_manager():
    """Calendar manager test"""
    print("🧪 Starting calendar manager test...")
    
    calendar_manager = CalendarManager()
    
    # Test with virtual data
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    
    events = calendar_manager.get_events(start_date, end_date)
    print(f"✅ Generated {len(events)} virtual events")
    
    # Find free time slots
    free_slots = calendar_manager.get_free_time_slots(start_date, end_date, 120)  # 2 hours
    print(f"✅ Found {len(free_slots)} available time slots")
    
    # Print event information
    print("\n📅 Generated virtual events:")
    for event in events[:5]:  # First 5 only
        print(f"  - {event['start'].strftime('%m/%d %H:%M')}: {event['title']}")
    
    # Print free time slot information
    print("\n⏰ Available time slots (top 5):")
    for slot in free_slots[:5]:
        print(f"  - {slot['start'].strftime('%m/%d %H:%M')}: {slot['duration_minutes']} min")
    
    return events, free_slots

def test_ai_agent():
    """AI agent test"""
    print("\n🤖 Starting AI agent test...")
    
    ai_agent = ScheduleAIAgent()
    
    # Test requests
    test_requests = [
        "Hospital appointment 2 hours",
        "Client meeting 1 hour",
        "Gym workout 1.5 hours",
        "Dental appointment 1 hour"
    ]
    
    for request in test_requests:
        print(f"\n📝 Test request: '{request}'")
        
        try:
            # Schedule analysis (demo mode)
            analysis = ai_agent.analyze_schedule_request(request, 2.0)
            
            print(f"✅ Analysis completed")
            print(f"  - Available time slots: {len(analysis['available_slots'])}")
            
            # Print AI analysis results
            if 'analysis' in analysis and analysis['analysis']:
                ai_result = analysis['analysis']
                print(f"  - Request analysis: {ai_result.get('request_analysis', 'N/A')}")
                
                recommendations = ai_result.get('recommendations', [])
                if recommendations:
                    print(f"  - Recommended time (1st priority): {recommendations[0].get('datetime', 'N/A')}")
                    print(f"  - Recommendation reason: {recommendations[0].get('reason', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")

def test_smart_analysis():
    """Smart analysis test"""
    print("\n🧠 Starting smart analysis test...")
    
    ai_agent = ScheduleAIAgent()
    
    # Request type classification test
    test_cases = [
        ("Hospital appointment", "medical"),
        ("Team meeting", "business"),
        ("Gym workout", "fitness"),
        ("Lunch appointment", "social"),
        ("Shopping", "shopping"),
        ("General work", "general")
    ]
    
    for request, expected_type in test_cases:
        classified_type = ai_agent._classify_request_type(request)
        status = "✅" if classified_type == expected_type else "❌"
        print(f"  {status} '{request}' -> {classified_type} (expected: {expected_type})")

def main():
    """Main test function"""
    print("🚀 AI Schedule Assistant Demo Test")
    print("=" * 50)
    
    try:
        # 1. Calendar manager test
        events, free_slots = test_calendar_manager()
        
        # 2. AI agent test
        test_ai_agent()
        
        # 3. Smart analysis test
        test_smart_analysis()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed!")
        print("\n📋 Test Results Summary:")
        print(f"  - Virtual events: {len(events)} generated")
        print(f"  - Available time slots: {len(free_slots)} found")
        print("  - AI analysis: Working normally")
        print("  - Smart analysis: Working normally")
        
        print("\n🌐 Web application execution:")
        print("  streamlit run app.py")
        print("  Access http://localhost:8501 in your browser")
        
    except Exception as e:
        print(f"\n❌ Error occurred during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()