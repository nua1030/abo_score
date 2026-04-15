import pymysql
import sys

# MariaDB 접속 정보
DB_HOST = "192.168.100.20"
DB_USER = "cjulib"
DB_PASS = "security"
DB_PORT = 3306
DB_NAME = "cju"

try:
    # 데이터베이스 연결
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        database=DB_NAME,  # cju 데이터베이스로 연결
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print(f"성공적으로 '{DB_NAME}' 데이터베이스에 접속했습니다!\n")
    
    


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
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 입력해주세요.")



                def update_member():
                    with conn.cursor() as cursor:
                        # 수정할 SQL 쿼리
                        sql = "UPDATE member SET name = %s WHERE seq = %s"

                        input_name = input('새로운 이름을 입력하세요: ')
                        input_seq = input('수정할 seq를 입력하세요: ')
                        
                        # 쿼리 실행
                        affected_rows = cursor.execute(sql, (input_name, input_seq))
                        
                        # 변경 사항 반영
                        conn.commit()
                        
                        if affected_rows > 0:
                            print(f"성공: seq가 '{input_seq}'인 사용자의 이름을 '{input_name}'으로 수정했습니다.")
                        else:
                            print(f"알림: seq가 '{input_seq}'인 사용자를 찾을 수 없어 수정되지 않았습니다.")

    if __name__ == "__main__":
        main_menu()

except pymysql.MySQLError as e:
    if 'conn' in locals():
        conn.rollback()
    print(f"오류 발생: {e}")
    sys.exit(1)

finally:
    if 'conn' in locals() and conn.open:
        conn.close()