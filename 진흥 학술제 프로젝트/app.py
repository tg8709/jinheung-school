from flask import Flask, render_template, request, redirect
# Flask는 웹 애플리케이션 프레임워크.
# render_template: HTML 템플릿을 렌더링.
# request: HTTP 요청 데이터에 접근.
# redirect: 특정 URL로 리다이렉트.

import sqlite3
# SQLite 데이터베이스를 사용하기 위한 모듈.

app = Flask(__name__)
# Flask 애플리케이션 생성. `__name__`은 현재 모듈 이름을 전달.

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # `database.db`라는 SQLite 데이터베이스 파일에 연결.
    conn.row_factory = sqlite3.Row
    # 행 데이터를 딕셔너리처럼 사용할 수 있도록 설정.
    return conn
    # 데이터베이스 연결 객체 반환.

@app.route('/')
def home():
    return render_template('index.html')
    # 루트 경로("/")로 요청이 들어오면 `index.html`을 렌더링하여 반환.

@app.route('/school-info')
def school_info():
    return render_template('school-info.html')
    # "/school-info" 경로 요청 시 `school-info.html`을 렌더링.

@app.route('/teachers')
def teachers():
    return render_template('teachers.html')
    # "/teachers" 경로 요청 시 `teachers.html`을 렌더링.

@app.route('/board', methods=['GET', 'POST'])
def board():
    if request.method == 'POST':
        # 게시판 페이지에서 POST 요청이 들어온 경우 (새 글 작성)
        title = request.form.get('title')
        # 입력받은 제목.
        content = request.form.get('content')
        # 입력받은 내용.
        
        if title and content:
            # 제목과 내용이 모두 있으면 데이터베이스에 저장.
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            # `posts` 테이블에 새 게시글 추가.
            conn.commit()
            # 변경 사항 저장.
            conn.close()
            # 데이터베이스 연결 닫기.
        return redirect('/board')
        # 게시판 페이지로 리다이렉트.

    # 게시글 목록을 최신 순으로 불러오기 (GET 요청 처리).
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    # `posts` 테이블에서 모든 게시글을 최신 순으로 가져옴.

    # 각 게시글에 해당하는 댓글 불러오기
    posts_with_comments = []
    for post in posts:
        # 모든 게시글에 대해 댓글을 가져옴.
        comments = conn.execute('SELECT * FROM comments WHERE post_id = ?', (post['id'],)).fetchall()
        # 각 게시글의 댓글 목록.
        post_data = dict(post)
        # 게시글 데이터를 딕셔너리로 변환.
        post_data['comments'] = comments
        # 게시글 데이터에 댓글 추가.
        posts_with_comments.append(post_data)
        # 댓글이 포함된 게시글 데이터를 리스트에 추가.

    conn.close()
    # 데이터베이스 연결 닫기.

    return render_template('board.html', posts=posts_with_comments)
    # `board.html` 템플릿에 게시글 데이터를 전달하여 렌더링.

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    comment_content = request.form.get('comment')
    # 입력받은 댓글 내용.

    if comment_content:
        # 댓글 내용이 있으면 데이터베이스에 저장.
        conn = get_db_connection()
        conn.execute('INSERT INTO comments (content, post_id) VALUES (?, ?)', (comment_content, post_id))
        # `comments` 테이블에 댓글 추가.
        conn.commit()
        # 변경 사항 저장.
        conn.close()
        # 데이터베이스 연결 닫기.

    return redirect('/board')
    # 게시판 페이지로 리다이렉트.

@app.route('/school-projects')
def school_projects():
    return render_template('school-projects.html')
    # "/school-projects" 경로 요청 시 `school-projects.html`을 렌더링.

@app.route('/school-local')
def school_local():
    return render_template('school-local.html')
    # "/school-local" 경로 요청 시 `school-local.html`을 렌더링.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # 애플리케이션 실행.
    # `debug=True`: 디버그 모드 활성화 (코드 변경 시 서버 자동 재시작).
    # `host='0.0.0.0'`: 모든 네트워크 인터페이스에서 접근 가능.
