
import mysql.connector
import json
import sys
from mysql.connector import Error
from datetime import datetime, timedelta

## 执行方式
# python3 select_data.py  '2025-07-18 00:00:00'   '2025-07-19 00:00:00'
start_date = sys.argv[1]
end_date = sys.argv[2]

class Error_Handler:
    def __init__(self):
        dbUser = "root"
        dbPass = "root2024@Nio"
        masterHost = "mr-mysql-prod-master.middleware.hlmd-prod.mysql.nioint.com"
        masterPort = 42226
        dbName = "hilreplay_infra"
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S') - timedelta(seconds=28800)
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') - timedelta(seconds=28800)
        print(self.start_date)
        print(self.end_date)
        self.connection = mysql.connector.connect(
            host=masterHost,
            port=masterPort,
            user=dbUser,
            password=dbPass,
            database=dbName
        )

    def insert_error(self, query):
        results = []
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor(dictionary=True)

                if "benchtaskdetail" in query: 
                    cursor.execute(query, (self.start_date, self.end_date))
                elif "errormapping" in query: 
                    cursor.execute(query)
                elif "queue" in query: 
                    cursor.execute(query)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                #print(f"查询结果:{results}")
        except Error as e:
            print("查询失败:", e)

        return results


    def pattern_errortype(self):
        error_num = {}
        error_info_list = []
        summary_num= 0
        queue_name = []
        queue_info = self.insert_error("""
        SELECT * FROM queue;
        """)

        error_info = self.insert_error("""
            SELECT * FROM benchtaskdetail
            WHERE created >= %s AND created < %s
            AND status = 2;
            """)
        error_pattern_results = self.insert_error("""
            SELECT * FROM errormapping;
            """)
        
        for row in queue_info:
            if row['isprod'] == 1:
                queue_name.append(row['name'])

        ## 取出错误信息到list
        for row in error_info:
            data = json.loads(row['errormsg'])
            error = data['error']
            plan_id = data['plan_id']
            task_queue_name = data['task_queue_name']
            if task_queue_name in queue_name:
                #if task_queue_name == "hil-replay-general-flexible-nt2aeb":
                    #print(row)
                error_info_list.append(error)
        
        ## 匹配错误类型
        for row in error_pattern_results:
          pattern = row['pattern']
          errortype = row['errortype']
          for error in error_info_list:
            if pattern in error:
                #print(f"{error} 匹配到 {pattern} 类型 {errortype}")
                error_num[errortype] = error_num.get(errortype, 0) + 1


        #print("=====================================================================================")
        ## 统计总数
        for key, value in error_num.items():
            summary_num = summary_num + value
        print(f"报错总数: {summary_num}")

        ## 统计各类型错误占比
        for key, value in error_num.items():
            print(f"{key} 类型错误数量: {value}, 类型错误占比: {value/summary_num*100:.2f}%")


    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()




error = Error_Handler()
error.pattern_errortype()
error.close_connection()


