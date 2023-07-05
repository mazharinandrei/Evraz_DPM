import datetime
from time import strptime

from django.shortcuts import render, get_object_or_404
from .models import Plan, Standart
from .forms import PlanForm, WorkShiftForm, PlanFormSet_without_extra, PlanFormSet_with_extra, FactForm
from django.forms import modelformset_factory
from django.db import connection


# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def plan(request):
    error = ''
    if request.method == 'POST':
        keys = list(request.POST.keys())
        smena_keys = keys[:2]
        forms_keys = keys[4:]
        #print(smena_keys)
        #print(forms_keys)

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id from work_shift "
                           f"where type_id = {request.POST[smena_keys[0]]} "
                           f"and date = \"{request.POST[smena_keys[1]]}\"")
            work_shift_id = cursor.fetchone()

        if work_shift_id == None:
            print('я здесь был')
            with connection.cursor() as cursor:
                cursor.execute(f"insert into work_shift (type_id, date) "
                               f"value ({request.POST[smena_keys[0]]}, "
                               f"\"{request.POST[smena_keys[1]]}\") ")

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id from work_shift "
                               f"where type_id = {request.POST[smena_keys[0]]} "
                               f"and date = \"{request.POST[smena_keys[1]]}\"")
                work_shift_id = cursor.fetchone()

        print(work_shift_id)

        with connection.cursor() as cursor:
            for i in range(4, len(forms_keys), 5):

                cursor.execute(
                    f"INSERT INTO plan "
                        f"(work_shift_id, "
                        f"hour, "
                        f"action_type_id, "
                        f"profile_id, "
                        f"time, "
                        f"volume) "
                    f"VALUES ('{work_shift_id[0]}', "
                            f"'{request.POST[forms_keys[i-4]]}', "
                            f"'{request.POST[forms_keys[i-3]]}', "
                            f"'{request.POST[forms_keys[i-2]]}', "
                            f"'{request.POST[forms_keys[i-1]]}', "
                            f"'{request.POST[forms_keys[i]]}')"
                )

    extra_plan = PlanFormSet_without_extra()

    if str(extra_plan) == "<input type=\"hidden\" name=\"form-TOTAL_FORMS\" value=\"0\" id=\"id_form-TOTAL_FORMS\"><input type=\"hidden\" name=\"form-INITIAL_FORMS\" value=\"0\" id=\"id_form-INITIAL_FORMS\"><input type=\"hidden\" name=\"form-MIN_NUM_FORMS\" value=\"0\" id=\"id_form-MIN_NUM_FORMS\"><input type=\"hidden\" name=\"form-MAX_NUM_FORMS\" value=\"1000\" id=\"id_form-MAX_NUM_FORMS\">":
        plan_form = PlanFormSet_with_extra()
    else:
        plan_form = PlanFormSet_without_extra()
    #print(plan_form)
    plan_form2 = PlanFormSet_without_extra()
    print("adfsadfsadfsadfsadfsadfsadfs")
    print(plan_form2)
    work_shift_form = WorkShiftForm()
    data = {
        'plan_form': plan_form,
        'work_shift_form': work_shift_form,
        'error': error
    }
    return render(request, 'main/plan.html', data)


def fact(request):
    date = datetime.datetime.now()
    now_hour = int((date - datetime.timedelta(hours=7)).strftime("%I"))  # Текущий час
    error = ''
    if request.method == 'POST':
        print(request.POST)
        aaa = dict(request.POST)
        times = [55,54,59,60]
        print(times)
        volumes = [90, 100, 111, 153]
        print(volumes)
        plan_ids = [1,2,3,4]

        forms = list(aaa.keys())
        print(forms)
        #for i in range(1, len(forms), 6):
            #print(request.POST[forms[i]])
            #plan_ids.append(request.POST[forms[i]])
        #print(plan_ids)
        with connection.cursor() as cursor:
            for i in range(len(plan_ids)):
                query = f"insert into fact(production_plan_id, time, volume)" \
                        f"value ({plan_ids[i]}, {times[i]}, {volumes[i]})"
                print(query)
                cursor.execute(query)
    extra_plan = PlanFormSet_without_extra()

    if str(extra_plan) == "<input type=\"hidden\" name=\"form-TOTAL_FORMS\" value=\"0\" id=\"id_form-TOTAL_FORMS\"><input type=\"hidden\" name=\"form-INITIAL_FORMS\" value=\"0\" id=\"id_form-INITIAL_FORMS\"><input type=\"hidden\" name=\"form-MIN_NUM_FORMS\" value=\"0\" id=\"id_form-MIN_NUM_FORMS\"><input type=\"hidden\" name=\"form-MAX_NUM_FORMS\" value=\"1000\" id=\"id_form-MAX_NUM_FORMS\">":
        plan_form = PlanFormSet_with_extra()
    else:
        plan_form = PlanFormSet_without_extra()
    fact_form = FactForm()
    work_shift_form = WorkShiftForm()
    data = {
        'plan_form': plan_form,
        'fact_form': fact_form,
        'work_shift_form': work_shift_form,
        'now_hour': now_hour,
        'error': error
    }
    return render(request, 'main/fact.html', data)


def dashboard(request):
    context = get_plan_fact(date=datetime.datetime.now())
    return render(request, 'main/dashboard.html', context)


def get_plan_fact(date):
    plan_now_perfomance = 0
    need_perfomance = 0
    #now_hour = int((date - datetime.timedelta(hours=7)).strftime("%I"))  # Текущий час
    now_hour=4
    print(f"Текущий час: {now_hour}")
    # Получение текущей смены !!!
    with connection.cursor() as cursor:
        """
        cursor.execute(f"SELECT profile.name,"
                           f"SUM(plan.volume),"
                           f"SUM(fact.volume) "
                       f"FROM fact "
                           f"JOIN plan ON production_plan_id = plan.id "
                           f"JOIN profile ON plan.profile_id = profile.id "
                           f"JOIN work_shift ON work_shift_id = work_shift.id "
                       f"WHERE date = \"{date.date()}\" "
                       f"GROUP BY profile.id")
        plan_fact = cursor.fetchall()
        
        # План/факт по профилям
        profiles = []           # Наименования профилей
        plan_volumes = []       # Планируемые объёмы производства по профилям
        fact_volumes = []       # Фактические объёмы производства по профилям
        plan_fact_diff = []     # Разница между планом и фактом производства по профилям

        # Производство на конец смены
        plan_end_predict = 0    # Производство на конец смены (планируемое)
        fact_end_predict = 0    # Производство на конец смены (фактическое)

        for item in plan_fact:
            profiles.append(item[0])
            plan_volumes.append(str(item[1]))
            fact_volumes.append(str(item[2]))
            plan_fact_diff.append(str(item[2] - item[1]))
            plan_end_predict += item[1]
        """
        dick = {}
        cursor.execute(f"SELECT "
                           f"plan.hour,"
                           f"action_type.name,"
                           f"profile.name, "
                           f"plan.volume as \"plan.volume\", "
                           f"plan.time as \"plan.time\","
                           f"IFNULL(fact.volume, 0) AS \"fact.volume\","
                           f"IFNULL(fact.time, 0) AS \"fact.time\""
                       f"FROM fact "
                           f"RIGHT JOIN plan ON production_plan_id = plan.id "
                           f"JOIN profile ON plan.profile_id = profile.id "
                           f"JOIN work_shift ON work_shift_id = work_shift.id "
                           f"JOIN action_type on action_type_id = action_type.id "
                       f"WHERE date = \"{date.date()}\" "
                       f"ORDER BY hour")
        query2 = cursor.fetchall()

    if query2 == None:
        return "Для начала сформируйте план и введите фактические данные"
    else:
        for item in query2:
            #print(item)
            standart = get_profile_standart(item[2])
            if item[2] not in dick.keys():
                dick[item[2]] = {
                    "plan_volumes": [],         # Планируемые объёмы на всю смену
                    "plan_volumes_now": [],     # Планируемые объёмы до текущего часа
                    "plan_time": [],            # Планируемое время
                    "fact_volumes": [],         # Фактические объёмы
                    "fact_time": [],            # Фактическое время
                    "time_left": [],            # Остаток времени
                    "predict_end": []          # Используется для прогноза на конец смены
                }
            dick[item[2]]["plan_volumes"].append(item[3])
            dick[item[2]]["plan_time"].append(item[4])
            dick[item[2]]["fact_volumes"].append(item[5])
            dick[item[2]]["fact_time"].append(item[6])
            time_left = 60-item[6]
            dick[item[2]]["time_left"].append(time_left)

            #dick[item[2]]["predict_end"].append((standart-item[5])*time_left/60)


            if item[0] <= now_hour:
                dick[item[2]]["plan_volumes_now"].append(item[3])

            if item[0] == now_hour:
                plan_now_perfomance = item[3]
                predict_now = standart * time_left / 60 # Сколько по нормативу успеет сделать за оставшееся время
            if item[0] >= now_hour:
                dick[item[2]]["predict_end"].append(standart)
        #print(dick)
        for key in dick.keys():
            dick[key]["sum_plan_volumes"] = sum(dick[key]["plan_volumes"])
            dick[key]["sum_plan_volumes_now"] = sum(dick[key]["plan_volumes_now"])
            dick[key]["sum_fact_volumes"] = sum(dick[key]["fact_volumes"])
            dick[key]["plan_fact_diff"] = (dick[key]["sum_fact_volumes"] - dick[key]["sum_plan_volumes_now"])

        #print(dick)

        profiles = dick.keys()
        plan_volumes_now = [dick[item]["sum_plan_volumes_now"] for item in dick.keys()]
        fact_volumes = [dick[item]["sum_fact_volumes"] for item in dick.keys()] # str
        plan_fact_diff = [dick[item]["plan_fact_diff"] for item in dick.keys()] # str
        plan_end = sum([dick[item]["sum_plan_volumes"] for item in dick.keys()])

        print(dick)
        sum_plan_volumes_now = sum(plan_volumes_now)


        production_now_predict = sum(fact_volumes) + predict_now

        production_end_predict = sum(fact_volumes) + sum([sum(dick[item]["predict_end"]) for item in dick.keys()])

        if now_hour < 12:
            need_perfomance = (plan_end - production_now_predict)/(12-now_hour)

        data = {
            "profiles": profiles,
            "plan_volumes_now": [str(item) for item in plan_volumes_now],
            "sum_plan_volumes_now": sum_plan_volumes_now,
            "fact_volumes": [str(item) for item in fact_volumes],
            "plan_fact_diff": [str(item) for item in plan_fact_diff],
            "plan_end": plan_end,
            "plan_now_perfomance": "%.2f" % plan_now_perfomance,
            "need_perfomance": "%.2f" % need_perfomance,
            "production_now_predict": "%.2f" % production_now_predict,
            "fact_end_predict": "%.2f" % production_end_predict,
            "plan_fact_diff_len": len(plan_fact_diff)
        }
        #print(data)
        return data

def get_profile_standart(name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT volume_in_hour "
                       f"FROM standart "
                       f"JOIN profile ON profile_id = profile.id "
                       f"WHERE name = \"{name}\"")

        return cursor.fetchone()[0]