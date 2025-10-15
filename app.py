import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from ai_agent import ScheduleAIAgent
from calendar_manager import CalendarManager
import config

# 페이지 설정
st.set_page_config(
    page_title="AI Schedule Assistant",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .event-card {
        background-color: #e8f4fd;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
        border-left: 3px solid #ff7f0e;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 헤더
    st.markdown('<h1 class="main-header">🤖 AI Schedule Assistant</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API 키 입력
        openai_key = st.text_input(
            "OpenAI API Key", 
            type="password",
            help="Enter your OpenAI API key. Demo mode uses virtual data."
        )
        
        if openai_key:
            config.OPENAI_API_KEY = openai_key
        
        st.markdown("---")
        
        # Demo mode toggle
        demo_mode = st.checkbox("Demo mode (use virtual data)", value=True)
        
        st.markdown("---")
        
        # Display current time
        st.subheader("📅 Current Time")
        current_time = datetime.now()
        st.write(f"**{current_time.strftime('%Y년 %m월 %d일 %H:%M')}**")
        
        st.markdown("---")
        
        # Calendar information
        st.subheader("📊 Calendar Information")
        calendar_manager = CalendarManager()
        
        # This week's event count
        week_start = current_time - timedelta(days=current_time.weekday())
        week_end = week_start + timedelta(days=6)
        events = calendar_manager.get_events(week_start, week_end)
        
        st.metric("This Week's Schedule", len(events))
        st.metric("Today's Schedule", len([e for e in events if e['start'].date() == current_time.date()]))
    
    # 메인 컨텐츠
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Schedule Request")
        
        # User input
        user_request = st.text_area(
            "What schedule would you like to plan?",
            placeholder="e.g., Hospital appointment 2 hours, Client meeting 1 hour, Gym workout 1.5 hours, etc.",
            height=100
        )
        
        col_duration, col_days = st.columns(2)
        
        with col_duration:
            duration_hours = st.slider(
                "Duration (hours)",
                min_value=0.5,
                max_value=8.0,
                value=2.0,
                step=0.5
            )
        
        with col_days:
            search_days = st.slider(
                "Search Period (days)",
                min_value=3,
                max_value=30,
                value=14,
                step=1
            )
        
        # Analysis button
        if st.button("🔍 Find Optimal Time", type="primary", use_container_width=True):
            if user_request:
                with st.spinner("AI is analyzing optimal time..."):
                    try:
                        # Initialize AI agent
                        ai_agent = ScheduleAIAgent()
                        
                        # Schedule analysis
                        if demo_mode or not openai_key:
                            # Demo mode - basic analysis only
                            analysis = ai_agent.analyze_schedule_request(user_request, duration_hours)
                        else:
                            # Real AI analysis
                            analysis = ai_agent.get_smart_suggestions(user_request, duration_hours)
                        
                        # Save results
                        st.session_state['analysis'] = analysis
                        st.session_state['user_request'] = user_request
                        st.session_state['duration'] = duration_hours
                        
                    except Exception as e:
                        st.error(f"An error occurred during analysis: {str(e)}")
            else:
                st.warning("Please enter a schedule request.")
    
    with col2:
        st.header("📋 Current Schedule")
        
        # Today's schedule
        today_events = [e for e in events if e['start'].date() == current_time.date()]
        
        if today_events:
            st.subheader("Today's Schedule")
            for event in today_events:
                st.markdown(f"""
                <div class="event-card">
                    <strong>{event['title']}</strong><br>
                    {event['start'].strftime('%H:%M')} - {event['end'].strftime('%H:%M')}<br>
                    <small>{event.get('location', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No scheduled events for today.")
        
        # This week's schedule summary
        st.subheader("This Week's Schedule Summary")
        if events:
            df_events = pd.DataFrame([
                {
                    'Date': event['start'].strftime('%m/%d'),
                    'Time': event['start'].strftime('%H:%M'),
                    'Title': event['title'],
                    'Duration': f"{int((event['end'] - event['start']).total_seconds() / 60)} min"
                }
                for event in events
            ])
            st.dataframe(df_events, use_container_width=True)
        else:
            st.info("No scheduled events for this week.")
    
    # 분석 결과 표시
    if 'analysis' in st.session_state:
        st.markdown("---")
        st.header("🎯 AI Analysis Results")
        
        analysis = st.session_state['analysis']
        
        # Request analysis
        st.subheader("📝 Request Analysis")
        st.write(analysis['analysis'].get('request_analysis', 'Unable to retrieve analysis results.'))
        
        # Recommended time
        st.subheader("⭐ Recommended Time")
        recommendations = analysis['analysis'].get('recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations[:3]):
                with st.container():
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h4>🥇 {i+1}st Priority Recommendation</h4>
                        <p><strong>Time:</strong> {rec.get('datetime', 'N/A')}</p>
                        <p><strong>Reason:</strong> {rec.get('reason', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No time slots available for recommendation.")
        
        # General advice
        if 'general_advice' in analysis['analysis']:
            st.subheader("💡 General Advice")
            st.info(analysis['analysis']['general_advice'])
        
        # Precautions
        if 'notes' in analysis['analysis']:
            st.subheader("⚠️ Precautions")
            st.warning(analysis['analysis']['notes'])
        
        # Available time slots chart
        if analysis['available_slots']:
            st.subheader("📊 Available Time Slots")
            
            # Prepare chart data
            chart_data = []
            for slot in analysis['available_slots'][:10]:  # Top 10 only
                chart_data.append({
                    'Date': slot['start'].strftime('%m/%d'),
                    'Time': slot['start'].strftime('%H:%M'),
                    'Available Time (min)': slot['duration_minutes'],
                    'Day': slot['start'].strftime('%A')
                })
            
            if chart_data:
                df_chart = pd.DataFrame(chart_data)
                
                # Bar chart
                fig = px.bar(
                    df_chart, 
                    x='Date', 
                    y='Available Time (min)',
                    color='Available Time (min)',
                    title="Available Time by Time Slot",
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed table
                st.subheader("📋 Detailed Time Slots")
                st.dataframe(df_chart, use_container_width=True)
        
        # Smart analysis results (if available)
        if 'smart_analysis' in analysis:
            smart = analysis['smart_analysis']
            
            st.subheader("🧠 Smart Analysis")
            
            col_type, col_pattern = st.columns(2)
            
            with col_type:
                st.metric("Request Type", smart.get('request_type', 'General'))
            
            with col_pattern:
                st.write("**Optimal Time Pattern:**")
                st.write(smart.get('best_time_pattern', 'N/A'))
            
            # Score-based recommendations
            if 'scored_slots' in smart:
                st.subheader("🎯 Score-based Recommendations")
                
                scored_data = []
                for slot in smart['scored_slots']:
                    scored_data.append({
                        'Time': slot['start'].strftime('%m/%d %H:%M'),
                        'Score': slot['score'],
                        'Reason': slot['reason']
                    })
                
                if scored_data:
                    df_scored = pd.DataFrame(scored_data)
                    
                    # Score chart
                    fig_score = px.bar(
                        df_scored,
                        x='Time',
                        y='Score',
                        color='Score',
                        title="Suitability Score by Time Slot",
                        color_continuous_scale='RdYlGn'
                    )
                    fig_score.update_layout(height=300)
                    st.plotly_chart(fig_score, use_container_width=True)
                    
                    # Score table
                    st.dataframe(df_scored, use_container_width=True)

if __name__ == "__main__":
    main()
