from flask import Flask, render_template_string, request, jsonify
from ai_agent import ScheduleAIAgent
from calendar_manager import CalendarManager
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI 스케줄 어시스턴트</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .content {
            padding: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        textarea {
            height: 100px;
            resize: vertical;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            opacity: 0.9;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        .recommendation {
            background: white;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #28a745;
        }
        .sidebar {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .event-item {
            background: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 3px;
            border-left: 3px solid #ffc107;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
    </style>
</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI 스케줄 어시스턴트</h1>
            <p>지능형 스케줄 관리 시스템</p>
        </div>
        
        <div class="content">
            <div class="sidebar">
                <h3>📅 현재 일정</h3>
                <div id="current-schedule">
                    <div class="loading">일정을 불러오는 중...</div>
                </div>
            </div>
            
            <form id="schedule-form">
                <div class="form-group">
                    <label for="request">스케줄 요청:</label>
                    <textarea id="request" name="request" placeholder="예: 병원 예약 2시간 소요, 고객 미팅 1시간, 헬스장 운동 1.5시간 등" required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="duration">소요 시간 (시간):</label>
                    <select id="duration" name="duration">
                        <option value="0.5">0.5시간</option>
                        <option value="1">1시간</option>
                        <option value="1.5">1.5시간</option>
                        <option value="2" selected>2시간</option>
                        <option value="3">3시간</option>
                        <option value="4">4시간</option>
                    </select>
                </div>
                
                <button type="submit">🔍 최적 시간 찾기</button>
            </form>
            
            <div id="result" class="result" style="display: none;">
                <h3>🎯 AI 분석 결과</h3>
                <div id="analysis-content"></div>
            </div>
        </div>
    </div>

    <script>
        // 현재 일정 로드
        fetch('/api/current-schedule')
            .then(response => response.json())
            .then(data => {
                const scheduleDiv = document.getElementById('current-schedule');
                if (data.events && data.events.length > 0) {
                    scheduleDiv.innerHTML = data.events.map(event => 
                        `<div class="event-item">
                            <strong>${event.title}</strong><br>
                            ${event.start} - ${event.end}<br>
                            <small>${event.location || ''}</small>
                        </div>`
                    ).join('');
                } else {
                    scheduleDiv.innerHTML = '<p>오늘 예정된 일정이 없습니다.</p>';
                }
            })
            .catch(error => {
                document.getElementById('current-schedule').innerHTML = '<p>일정을 불러올 수 없습니다.</p>';
            });

        // 폼 제출 처리
        document.getElementById('schedule-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const request = document.getElementById('request').value;
            const duration = document.getElementById('duration').value;
            
            if (!request.trim()) {
                alert('스케줄 요청을 입력해주세요.');
                return;
            }
            
            // 로딩 표시
            const resultDiv = document.getElementById('result');
            const contentDiv = document.getElementById('analysis-content');
            resultDiv.style.display = 'block';
            contentDiv.innerHTML = '<div class="loading">AI가 최적의 시간을 분석 중입니다...</div>';
            
            // API 호출
            fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    request: request,
                    duration: parseFloat(duration)
                })
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                contentDiv.innerHTML = '<p style="color: red;">분석 중 오류가 발생했습니다.</p>';
            });
        });
        
        function displayResults(data) {
            const contentDiv = document.getElementById('analysis-content');
            
            let html = `
                <h4>📝 요청 분석</h4>
                <p>${data.analysis.request_analysis}</p>
                
                <h4>⭐ 추천 시간</h4>
            `;
            
            if (data.analysis.recommendations && data.analysis.recommendations.length > 0) {
                data.analysis.recommendations.forEach((rec, index) => {
                    html += `
                        <div class="recommendation">
                            <h5>🥇 ${index + 1}순위 추천</h5>
                            <p><strong>시간:</strong> ${rec.datetime}</p>
                            <p><strong>이유:</strong> ${rec.reason}</p>
                        </div>
                    `;
                });
            } else {
                html += '<p>추천할 수 있는 시간이 없습니다.</p>';
            }
            
            if (data.analysis.general_advice) {
                html += `<h4>💡 일반 조언</h4><p>${data.analysis.general_advice}</p>`;
            }
            
            if (data.analysis.notes) {
                html += `<h4>⚠️ 주의사항</h4><p>${data.analysis.notes}</p>`;
            }
            
            contentDiv.innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/current-schedule')
def get_current_schedule():
    try:
        calendar_manager = CalendarManager()
        current_time = datetime.now()
        week_start = current_time - timedelta(days=current_time.weekday())
        week_end = week_start + timedelta(days=6)
        
        events = calendar_manager.get_events(week_start, week_end)
        
        # 오늘의 이벤트만 필터링
        today_events = []
        for event in events:
            if event['start'].date() == current_time.date():
                today_events.append({
                    'title': event['title'],
                    'start': event['start'].strftime('%H:%M'),
                    'end': event['end'].strftime('%H:%M'),
                    'location': event.get('location', '')
                })
        
        return jsonify({'events': today_events})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/analyze', methods=['POST'])
def analyze_schedule():
    try:
        data = request.get_json()
        user_request = data.get('request', '')
        duration_hours = data.get('duration', 2.0)
        
        if not user_request:
            return jsonify({'error': '스케줄 요청이 필요합니다.'})
        
        ai_agent = ScheduleAIAgent()
        analysis = ai_agent.analyze_schedule_request(user_request, duration_hours)
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 AI 스케줄 어시스턴트 웹 서버 시작")
    print("📱 브라우저에서 http://localhost:5000 접속")
    app.run(debug=True, host='0.0.0.0', port=5000)
