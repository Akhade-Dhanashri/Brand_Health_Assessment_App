import sqlite3
import csv

DB_FILE = "submissions.db"
EXPORT_TO_CSV = True  # Set to False if you don’t want to export

def view_submissions():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM submissions")
        rows = cursor.fetchall()

        if not rows:
            print("📭 No submissions found.")
            return

        print("\n📋 All Submissions:")
        print("-" * 60)
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Email: {row[2]}")
            print(f"Company: {row[3]}")
            print(f"Responses: {row[4]}")
            print(f"Score: {row[5]}")
            print("-" * 60)

        if EXPORT_TO_CSV:
            with open("submissions_export.csv", mode="w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Email", "Company", "Responses", "Score"])
                writer.writerows(rows)
            print("✅ Data exported to 'submissions_export.csv'.")

        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    view_submissions()
