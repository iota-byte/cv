from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)

# MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',  # Replace with your MySQL username
        password='your_password',  # Replace with your MySQL password
        database='todo_db'  # Ensure this matches the database name you created
    )
    return connection


# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data['title']
    description = data.get('description', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (title, description) VALUES (%s, %s)',
        (title, description)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': task_id, 'title': title, 'description': description})

# Update a task's completion status
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    completed = data['completed']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tasks SET completed = %s WHERE id = %s',
        (completed, task_id)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task updated successfully'})

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
