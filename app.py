"""
Databricks Lakebase Ticketing System Viewer:
- Flask API to view tickets and ticket messages from Lakebase
- Reads from 'tickets' and 'ticket_messages' tables
- Simple HTML interface for viewing ticket data
"""

import logging
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
import lakebase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ticketing-viewer")

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Disable authentication check for development
app.config['TESTING'] = False

# Simple HTML template for the UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Lakebase Ticketing System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .ticket { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .ticket-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .ticket-title { font-size: 18px; font-weight: bold; color: #1a73e8; }
        .ticket-status { padding: 5px 10px; border-radius: 3px; font-size: 12px; font-weight: bold; }
        .status-open { background: #fff3cd; color: #856404; }
        .status-in_progress { background: #cfe2ff; color: #084298; }
        .status-closed { background: #d1e7dd; color: #0f5132; }
        .ticket-meta { color: #666; font-size: 14px; margin: 5px 0; }
        .messages { margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd; }
        .message { margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 3px solid #1a73e8; }
        .message-author { font-weight: bold; color: #333; }
        .message-time { color: #666; font-size: 12px; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .filters { background: white; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
        select { padding: 8px; margin: 0 10px; border-radius: 3px; border: 1px solid #ddd; }
        button { padding: 8px 15px; background: #1a73e8; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #1557b0; }
    </style>
</head>
<body>
    <h1>🎫 Lakebase Ticketing System</h1>
    
    <div class="filters">
        <form method="get">
            <label>Status:</label>
            <select name="status">
                <option value="">All</option>
                <option value="open" {{ 'selected' if status == 'open' else '' }}>Open</option>
                <option value="in_progress" {{ 'selected' if status == 'in_progress' else '' }}>In Progress</option>
                <option value="closed" {{ 'selected' if status == 'closed' else '' }}>Closed</option>
            </select>
            
            <button type="submit">Filter</button>
        </form>
    </div>
    
    {% if error %}
    <div class="error">
        <strong>Error:</strong> {{ error }}
        <p>Please ensure the 'tickets' and 'ticket_messages' tables exist in your Lakebase database.</p>
    </div>
    {% else %}
    <p><strong>{{ tickets|length }}</strong> ticket(s) found</p>
    
    {% for ticket in tickets %}
    <div class="ticket">
        <div class="ticket-header">
            <div class="ticket-title">#{{ ticket.ticket_id }} - {{ ticket.title }}</div>
            <span class="ticket-status status-{{ ticket.status }}">{{ ticket.status.upper().replace('_', ' ') }}</span>
        </div>
        
        <div class="ticket-meta">
            <strong>Created by:</strong> {{ ticket.created_by }}
        </div>
        <div class="ticket-meta">
            <strong>Created:</strong> {{ ticket.created_at }}
        </div>
        
        {% if ticket.messages %}
        <div class="messages">
            <strong>Messages ({{ ticket.messages|length }}):</strong>
            {% for msg in ticket.messages %}
            <div class="message">
                <div class="message-author">{{ msg.created_by }} <span class="message-time">({{ msg.created_at }})</span></div>
                <div>{{ msg.message }}</div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    {% endfor %}
    {% endif %}
</body>
</html>
"""


@app.route("/healthz")
def healthz():
    logger.info("Health endpoint called")
    return jsonify({"status": "ok"})


@app.errorhandler(Exception)
def handle_exception(err):
    """Ensure all unhandled errors return JSON"""
    logger.exception("Unhandled exception while processing request")
    status_code = getattr(err, "code", 500)
    if not isinstance(status_code, int):
        status_code = 500
    return jsonify({"error": str(err)}), status_code


@app.route("/")
def index():
    logger.info("Entered index()")
    """Main UI - display tickets with filters"""
    try:
        # Get filter parameters
        status_filter = request.args.get('status', '')
        
        # Build query with filters
        query = """
            SELECT 
                ticket_id,
                title,
                status,
                created_by,
                created_at
            FROM tickets
            WHERE 1=1
        """
        params = []
        
        if status_filter:
            query += " AND status = %s"
            params.append(status_filter)
        
        query += " ORDER BY created_at DESC"
        logger.info("Fetching tickets from Lakebase...")
        # Fetch tickets
        tickets = lakebase.run_query(query, tuple(params) if params else None)
        logger.info(f"Fetched {len(tickets)} tickets")
        
        # Fetch messages for each ticket
        for ticket in tickets:
            logger.info(f"Fetched {len(tickets)} tickets")
            messages = lakebase.run_query(
                """
                SELECT message_id as id, ticket_id, message_text as message, author as created_by, created_at
                FROM ticket_messages
                WHERE ticket_id = %s
                ORDER BY created_at ASC
                """,
                (ticket['ticket_id'],)
            )
            ticket['messages'] = messages
            logger.info("Messages fetched successfully")
        return render_template_string(
            HTML_TEMPLATE,
            tickets=tickets,
            status=status_filter,
            error=None
        )
        
    except Exception as e:
        logger.exception("Exception inside index()")
        return render_template_string(
            HTML_TEMPLATE,
            tickets=[],
            status='',
            error=str(e)
        )


@app.route("/api/tickets")
def api_tickets():
    """API endpoint to get tickets as JSON"""
    try:
        tickets = lakebase.run_query(
            """
            SELECT 
                ticket_id,
                title,
                status,
                created_by,
                created_at
            FROM tickets
            ORDER BY created_at DESC
            """
        )
        return jsonify(tickets)
    except Exception as e:
        logger.exception("Error fetching tickets")
        return jsonify({"error": str(e)}), 500


@app.route("/api/tickets/<ticket_id>/messages")
def api_ticket_messages(ticket_id):
    """API endpoint to get messages for a specific ticket"""
    try:
        messages = lakebase.run_query(
            """
            SELECT message_id as id, ticket_id, message_text as message, author as created_by, created_at
            FROM ticket_messages
            WHERE ticket_id = %s
            ORDER BY created_at ASC
            """,
            (ticket_id,)
        )
        return jsonify(messages)
    except Exception as e:
        logger.exception(f"Error fetching messages for ticket {ticket_id}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
