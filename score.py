import pymysql
import sys

# MariaDB 접속 정보
DB_HOST = "192.168.100.20"
DB_USER = "cjulib"
DB_PASS = "security"
DB_PORT = 3306
DB_NAME = "cju"


# 1. 전체조회
def select_all():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            sql = """
            SELECT g.id_grade, m.name, m.id, g.subject, g.score, g.term, DATE(g.reg_date) AS reg_date
            FROM member m
            JOIN grades g ON m.seq = g.member_seq
            ORDER BY g.id_grade
            """
            cursor.execute(sql)
            result = cursor.fetchall()

            print("\n--- [ 성적 전체 목록 ] ---")
            print("번호 | 이름(ID) | 과목명 | 점수 | 학기 | 등록일")
            print("-----------------------------------------------------------")

            for row in result:
                print(f"{row['id_grade']} | {row['name']}({row['id']}) | {row['subject']} | {row['score']} | {row['term']} | {row['reg_date']}")

            print("-----------------------------------------------------------")

    except pymysql.MySQLError as e:
        print(f"오류 발생: {e}")
        sys.exit(1)

    finally:
        if 'conn' in locals() and conn.open:
            conn.close()


# 2. 번호조회
def select_one():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        seq = input("조회할 학생 번호(seq) 입력: ")

        with conn.cursor() as cursor:
            sql = """
            SELECT m.name, m.id, g.subject, g.score, g.term
            FROM member m
            JOIN grades g ON m.seq = g.member_seq
            WHERE m.seq = %s
            """
            cursor.execute(sql, (seq,))
            result = cursor.fetchall()

            if len(result) == 0:
                print("해당 학생의 성적이 없습니다.")
                return

            print(f"\n--- [ {result[0]['name']} 학생의 성적 리포트 ] ---")
            print(f"- 아이디: {result[0]['id']}")
            print(f"- 학기: {result[0]['term']}")
            print("---------------------------")

            total = 0
            count = 0

            for i, row in enumerate(result, start=1):
                print(f"{i}. {row['subject']}: {row['score']}점")
                total += row['score']
                count += 1

            avg = total / count
            print("---------------------------")
            print(f"평균 점수: {avg:.1f}점")

    except pymysql.MySQLError as e:
        print(f"오류 발생: {e}")
        sys.exit(1)

    finally:
        if 'conn' in locals() and conn.open:
            conn.close()


# 3. 성적 추가
def insert_member():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        print("\n--- [ 성적 데이터 추가 ] ---")
        member_seq = input("- 학생 번호(seq) 입력: ")
        subject = input("- 과목명 입력: ")
        score = input("- 점수 입력: ")
        term = input("- 학기 입력(예: 2026-1): ")

        with conn.cursor() as cursor:
            sql_name = "SELECT name FROM member WHERE seq = %s"
            cursor.execute(sql_name, (member_seq,))
            student = cursor.fetchone()

            sql = "INSERT INTO grades (member_seq, subject, score, term) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (member_seq, subject, score, term))
            conn.commit()

            print(f"\n[시스템] '{student['name']}' 학생의 '{subject}' 성적이 성공적으로 등록되었습니다.")

    except pymysql.MySQLError as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"오류 발생: {e}")
        sys.exit(1)

    finally:
        if 'conn' in locals() and conn.open:
            conn.close()


# 4. 성적 삭제
def delete_member():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        id_grade = input("삭제할 성적의 고유 ID(id_grade) 입력: ")

        with conn.cursor() as cursor:
            sql_check = "SELECT * FROM grades WHERE id_grade = %s"
            cursor.execute(sql_check, (id_grade,))
            result = cursor.fetchone()

            if result is None:
                print("해당 성적 데이터가 없습니다.")
                return

            confirm = input("정말로 삭제하시겠습니까? (y/n): ")

            if confirm == 'y':
                sql = "DELETE FROM grades WHERE id_grade = %s"
                cursor.execute(sql, (id_grade,))
                conn.commit()
                print(f"\n[시스템] {id_grade}번 성적 데이터가 삭제되었습니다. (대상: {result['subject']})")
            else:
                print("삭제가 취소되었습니다.")

    except pymysql.MySQLError as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"오류 발생: {e}")
        sys.exit(1)

    finally:
        if 'conn' in locals() and conn.open:
            conn.close()


# 5. 성적 수정
def update_member():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        id_grade = input("수정할 성적의 고유 ID(id_grade) 입력: ")

        with conn.cursor() as cursor:
            sql_check = "SELECT * FROM grades WHERE id_grade = %s"
            cursor.execute(sql_check, (id_grade,))
            result = cursor.fetchone()

            if result is None:
                print("해당 성적 데이터가 없습니다.")
                return

            print(f"--- 현재 정보: {result['subject']} ({result['score']}점) ---")
            new_score = input("- 수정할 점수 입력: ")

            sql = "UPDATE grades SET score = %s WHERE id_grade = %s"
            cursor.execute(sql, (new_score, id_grade))
            conn.commit()

            print(f"\n[시스템] 성적 수정이 완료되었습니다. ({result['score']}점 -> {new_score}점)")

    except pymysql.MySQLError as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"오류 발생: {e}")
        sys.exit(1)

    finally:
        if 'conn' in locals() and conn.open:
            conn.close()


# 메인 메뉴 루프
def main_menu():
    while True:
        print("\n--- [ 성적 관리 시스템 ] ---")
        print("1. 전체조회")
        print("2. 번호조회")
        print("3. 성적 추가")
        print("4. 성적 삭제")
        print("5. 성적 수정")
        print("6. 종료")
        print("---------------------------")

        choice = input("메뉴 선택: ")

        if choice == '1':
            select_all()
        elif choice == '2':
            select_one()
        elif choice == '3':
            insert_member()
        elif choice == '4':
            delete_member()
        elif choice == '5':
            update_member()
        elif choice == '6':
            print("프로그램을 종료합니다. 감사합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")


if __name__ == "__main__":
    main_menu()