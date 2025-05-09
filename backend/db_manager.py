#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0644u0645u0634u0631u0648u0639 Horus AI Pipeline

u064au0648u0641u0631 u0647u0630u0627 u0627u0644u0645u0644u0641 u0648u0627u062cu0647u0629 u0644u0644u062au0639u0627u0645u0644 u0645u0639 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a MySQL u0627u0644u062eu0627u0635u0629 u0628u0627u0644u0645u0634u0631u0648u0639.
"""

import mysql.connector
import logging
from mysql.connector import pooling
from datetime import datetime
import json
from db_config import DB_CONFIG, CONNECTION_SETTINGS

# u0625u0639u062fu0627u062f u0627u0644u062au0633u062cu064au0644
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("database.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("db_manager")

class DatabaseManager:
    """u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0644u0644u062au0639u0627u0645u0644 u0645u0639 u0642u0627u0639u062fu0629 u0628u064au0627u0646u0627u062a MySQL"""
    
    _instance = None
    
    def __new__(cls):
        """u0646u0645u0637 Singleton u0644u0636u0645u0627u0646 u0648u062cu0648u062f u0646u0633u062eu0629 u0648u0627u062du062fu0629 u0641u0642u0637 u0645u0646 u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a"""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """u062au0647u064au0626u0629 u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a"""
        try:
            # u0625u0646u0634u0627u0621 u062au062cu0645u0639 u0627u062au0635u0627u0644u0627u062a
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="horus_pool",
                pool_size=CONNECTION_SETTINGS.get("pool_size", 5),
                **DB_CONFIG
            )
            logger.info("u062au0645 u0625u0646u0634u0627u0621 u062au062cu0645u0639 u0627u062au0635u0627u0644u0627u062a u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0628u0646u062cu0627u062d")
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u0625u0646u0634u0627u0621 u062au062cu0645u0639 u0627u062au0635u0627u0644u0627u062a u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a: {err}")
            raise
    
    def get_connection(self):
        """u0627u0644u062du0635u0648u0644 u0639u0644u0649 u0627u062au0635u0627u0644 u0645u0646 u062au062cu0645u0639 u0627u0644u0627u062au0635u0627u0644u0627u062a"""
        try:
            return self.connection_pool.get_connection()
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u0627u0644u062du0635u0648u0644 u0639u0644u0649 u0627u062au0635u0627u0644 u0645u0646 u062au062cu0645u0639 u0627u0644u0627u062au0635u0627u0644u0627u062a: {err}")
            raise
    
    # u0639u0645u0644u064au0627u062a u0627u0644u062cu0644u0633u0627u062a
    def create_session(self, summary=None):
        """u0625u0646u0634u0627u0621 u062cu0644u0633u0629 u062cu062fu064au062fu0629"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "INSERT INTO sessions (session_summary) VALUES (%s)"
            cursor.execute(query, (summary,))
            session_id = cursor.lastrowid
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"u062au0645 u0625u0646u0634u0627u0621 u062cu0644u0633u0629 u062cu062fu064au062fu0629 u0628u0645u0639u0631u0641 {session_id}")
            return session_id
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u0625u0646u0634u0627u0621 u062cu0644u0633u0629 u062cu062fu064au062fu0629: {err}")
            return None
    
    def end_session(self, session_id):
        """u0625u0646u0647u0627u0621 u062cu0644u0633u0629 u0628u062au0639u064au064au0646 u0648u0642u062a u0627u0644u0627u0646u062au0647u0627u0621"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "UPDATE sessions SET end_time = CURRENT_TIMESTAMP WHERE session_id = %s"
            cursor.execute(query, (session_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"u062au0645 u0625u0646u0647u0627u0621 u0627u0644u062cu0644u0633u0629 u0628u0645u0639u0631u0641 {session_id}")
            return True
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u0625u0646u0647u0627u0621 u0627u0644u062cu0644u0633u0629: {err}")
            return False
    
    def get_session(self, session_id):
        """u0627u0644u062du0635u0648u0644 u0639u0644u0649 u0645u0639u0644u0648u0645u0627u062a u062cu0644u0633u0629"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM sessions WHERE session_id = %s"
            cursor.execute(query, (session_id,))
            session = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return session
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u0627u0644u062du0635u0648u0644 u0639u0644u0649 u0645u0639u0644u0648u0645u0627u062a u0627u0644u062cu0644u0633u0629: {err}")
            return None
    
    # u0639u0645u0644u064au0627u062a u0627u0644u0631u0633u0627u0626u0644
    def add_message(self, session_id, sender, content):
        """u0625u0636u0627u0641u0629 u0631u0633u0627u0644u0629 u062cu062fu064au062fu0629 u0625u0644u0649 u062cu0644u0633u0629"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # u062au062du0648u064au0644 u0627u0644u0645u062du062au0648u0649 u0625u0644u0649 JSON u0625u0630u0627 u0643u0627u0646 u0642u0627u0645u0648u0633u0627u064b u0623u0648 u0642u0627u0626u0645u0629
            if isinstance(content, (dict, list)):
                content = json.dumps(content, ensure_ascii=False)
            
            query = "INSERT INTO messages (session_id, sender, content) VALUES (%s, %s, %s)"
            cursor.execute(query, (session_id, sender, content))
            message_id = cursor.lastrowid
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"u062au0645u062a u0625u0636u0627u0641u0629 u0631u0633u0627u0644u0629 u062cu062fu064au062fu0629 u0628u0645u0639u0631u0641 {message_id} u0625u0644u0649 u0627u0644u062cu0644u0633u0629 {session_id}")
            return message_id
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u0625u0636u0627u0641u0629 u0631u0633u0627u0644u0629: {err}")
            return None
    
    def get_session_messages(self, session_id):
        """u0627u0644u062du0635u0648u0644 u0639u0644u0649 u062cu0645u064au0639 u0631u0633u0627u0626u0644 u062cu0644u0633u0629"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM messages WHERE session_id = %s ORDER BY timestamp ASC"
            cursor.execute(query, (session_id,))
            messages = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # u0645u062du0627u0648u0644u0629 u062au062du0648u064au0644 u0645u062du062au0648u0649 JSON u0625u0644u0649 u0643u0627u0626u0646u0627u062a Python
            for message in messages:
                try:
                    message['content'] = json.loads(message['content'])
                except (json.JSONDecodeError, TypeError):
                    # u0625u0630u0627 u0644u0645 u064au0643u0646 JSON u0635u0627u0644u062du0627u064bu060c u0627u062au0631u0643u0647 u0643u0645u0627 u0647u0648
                    pass
            
            return messages
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u0627u0644u062du0635u0648u0644 u0639u0644u0649 u0631u0633u0627u0626u0644 u0627u0644u062cu0644u0633u0629: {err}")
            return []
    
    # u0639u0645u0644u064au0627u062a u0627u0644u0627u0633u062au0639u0644u0627u0645 u0627u0644u0639u0627u0645u0629
    def test_connection(self):
        """u062au062du0648u0644 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result and result[0] == 1:
                logger.info("u062au0645 u062au062du0648u0644 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0628u0646u062cu0627u062d")
                return True
            else:
                logger.warning("u0641u0634u0644 u062au062du0648u0644 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a")
                return False
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a: {err}")
            return False
    
    def execute_query(self, query, params=None):
        """u062au0646u0641u064au0630 u0627u0633u062au0639u0644u0627u0645 SQL u0645u062eu0635u0635"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # u0625u0630u0627 u0643u0627u0646 u0627u0644u0627u0633u062au0639u0644u0627u0645 SELECT
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = {"affected_rows": cursor.rowcount, "last_insert_id": cursor.lastrowid}
            
            cursor.close()
            conn.close()
            
            return result
        except mysql.connector.Error as err:
            logger.error(f"u062eu0637u0623 u0641u064a u062au0646u0641u064au0630 u0627u0644u0627u0633u062au0639u0644u0627u0645: {err}")
            return None

# u0645u062bu0627u0644 u0639u0644u0649 u0627u0644u0627u0633u062au062eu062fu0627u0645
def example_usage():
    """u0645u062bu0627u0644 u0639u0644u0649 u0627u0633u062au062eu062fu0627u0645 u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a"""
    try:
        # u0625u0646u0634u0627u0621 u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
        db_manager = DatabaseManager()
        
        # u0625u0646u0634u0627u0621 u062cu0644u0633u0629 u062cu062fu064au062fu0629
        session_id = db_manager.create_session("u062cu0644u0633u0629 u0627u062eu062au0628u0627u0631")
        print(f"u062au0645 u0625u0646u0634u0627u0621 u062cu0644u0633u0629 u062cu062fu064au062fu0629 u0628u0645u0639u0631u0641: {session_id}")
        
        # u0625u0636u0627u0641u0629 u0631u0633u0627u0626u0644
        db_manager.add_message(session_id, "user", "u0645u0631u062du0628u0627u064b! u0643u064au0641 u064au0645u0643u0646u0646u064a u0627u0633u062au062eu062fu0627u0645 u0627u0644u0646u0638u0627u0645u061f")
        db_manager.add_message(session_id, "ai", "u0645u0631u062du0628u0627u064b u0628u0643! u064au0645u0643u0646u0643 u0627u0633u062au062eu062fu0627u0645 u0627u0644u0646u0638u0627u0645 u0644u0644u062au0641u0627u0639u0644 u0645u0639 u0646u0645u0627u0630u062c u0627u0644u0630u0643u0627u0621 u0627u0644u0627u0635u0637u0646u0627u0639u064a u0627u0644u0645u062eu062au0644u0641u0629.")
        
        # u0627u0644u062du0635u0648u0644 u0639u0644u0649 u0631u0633u0627u0626u0644 u0627u0644u062cu0644u0633u0629
        messages = db_manager.get_session_messages(session_id)
        print(f"u0639u062fu062f u0627u0644u0631u0633u0627u0626u0644 u0641u064a u0627u0644u062cu0644u0633u0629: {len(messages)}")
        for msg in messages:
            print(f"{msg['sender']}: {msg['content']}")
        
        # u0625u0646u0647u0627u0621 u0627u0644u062cu0644u0633u0629
        db_manager.end_session(session_id)
        print(f"u062au0645 u0625u0646u0647u0627u0621 u0627u0644u062cu0644u0633u0629 {session_id}")
        
    except Exception as e:
        print(f"u062du062fu062b u062eu0637u0623: {e}")

if __name__ == "__main__":
    # u0627u062eu062au0628u0627u0631 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
    try:
        db_manager = DatabaseManager()
        print("u062au0645 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0628u0646u062cu0627u062d!")
        
        # u062au0634u063au064au0644 u0645u062bu0627u0644 u0627u0644u0627u0633u062au062eu062fu0627u0645
        print("\n=== u0645u062bu0627u0644 u0639u0644u0649 u0627u0633u062au062eu062fu0627u0645 u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a ===")
        example_usage()
    except Exception as e:
        print(f"u062eu0637u0623 u0641u064a u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a: {e}")
