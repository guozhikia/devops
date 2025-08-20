#!/bin/python3
import requests
import sys

plan_id = sys.argv[1]
print(plan_id)

class GetCoredumpInfo():
    def __init__(self) -> None:
        self.plan_id = plan_id
        self.result_data = self.get_all_info()
        self.sum_num = 0

    def get_all_info(self):
        url = f"http://adsim-metrics-api.nioint.com/metrics/hil_replay/case/table_list?exec_plan_id={self.plan_id}&created=0&page_size=1000&page=0"
        response = requests.get(url)
        if response.status_code == 200:
            raw_data = response.json()
            result_data = response.json()['data']
        else:
            raise Exception(f"{self.plan_id}获取数据失败")
        # print(result_data)
        return result_data

    def get_need_info(self):
        self.result_data['content']
        num = len(self.result_data['content'])
        for i in range(0, num):
            line = self.result_data['content'][i]
            case_id = line['case_id']
            #print(line)
            #task_id = line['id']
            # print(case_id)
            try_num = len(line['common_fields'])
            # print(try_num)
            self.sum_num = self.sum_num + try_num
            for i in range(0, try_num):
                checkers_result = line['common_fields'][i]['checkers_result']
                task_id = line['common_fields'][i]['id']
                # print(line['common_fields'][i]['checkers_result'])
                #print(i,checkers_result)
                if checkers_result == {}:
                    self.sum_num = self.sum_num - 1 
                    continue
            #    if checkers_result['valid_test']['pass'] == False:
            #        continue

                #pass_or_fail_urban = checkers_result['urban']['pass']
                #pass_or_fail_psp = checkers_result['psp']['pass']
                #pass_or_fail_nop = checkers_result['nop']['pass']
                if checkers_result.get('urban'):
                    functions = 'urban'
                    pass_or_fail = checkers_result['urban']['pass']
                elif checkers_result.get('nop'):
                    functions = 'nop'
                    pass_or_fail = checkers_result['nop']['pass']
                #print(checkers_result['valid_test']['pass'])
                if not checkers_result['valid_test']['pass']:
                    continue
                server_ip = str(checkers_result['version']['info']['bench_ip']).strip()
                if "10" in server_ip:
                    if pass_or_fail == True:
                        trigger_percentage = checkers_result[functions]['info']['replay_activate_time/origin_activate_time(%)']
                        #print(case_id, task_id, "urban触发", trigger_percentage)
                        print(case_id, task_id, f"{functions}触发", trigger_percentage, server_ip)
                #elif pass_or_fail_psp == True:
                #    print(case_id, "psp触发")
                #elif pass_or_fail_nop == True:
                #    print(case_id, "nop触发")
                    else:
                        #print(case_id, task_id, "不触发")
                        print(case_id, task_id, "不触发", "      ",server_ip)
                # print(checkers_result['coredump']['pass'])

        #         if checkers_result.get('coredump',None) == None:
        #             continue
        #         pass_or_fail = checkers_result['coredump']['pass']
        #         if pass_or_fail == False:
        #             # print(checkers_result['coredump']['info']['coredumps'])
        #             core_info = dict(checkers_result['coredump']['info']['coredumps'])
        #             for soc, info in core_info.items():
        #                 if info != []:
        #                     print(soc, info)

        #             print("coredump_url: ", line['common_fields'][i]['coredumps_zip_url'])
        #             print("logs_url: ", line['common_fields'][i]['download_url'])
        # print(int(self.sum_num) * 5 )

                







get_info=GetCoredumpInfo()
get_info.get_need_info()







