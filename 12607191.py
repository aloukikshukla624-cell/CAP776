import openpyxl as xl


def load_data(xl_file):
    wb = xl.load_workbook(xl_file, data_only = True)
    ws = wb['Daily Log']

    expectDays = 36
    MyData = []

    for row in range(6, ws.max_row + 1):
        date = ws.cell(row, column = 1).value

        if date is not None:
            log = {
                "date" : date,
                "sleep" : ws.cell(row, column = 2).value,
                "fitness" : ws.cell(row, column = 3).value,
                "study" : ws.cell(row, column = 4).value,
                "coding" : ws.cell(row, column = 5).value,
                "class" : ws.cell(row, column = 6).value,
                "classesAttended" : ws.cell(row, column = 7).value,
                "otherActivity" : ws.cell(row, column = 8).value,
                "totalTrackedTime" : ws.cell(row, column = 9).value,
                "unaccounted" : ws.cell(row, column = 10).value,
                "Feeling" : ws.cell(row, column = 11).value,
                "Satisfaction" : ws.cell(row, column = 12).value,
                "Energy" : ws.cell(row, column = 13).value,
            }

            MyData.append(log)

    wb.close()

    experience = {
                   "Feeling" : {
                       'Excellent' : 5, 
                       'Good' : 4, 
                       'Neutral' : 3, 
                       'Low' : 2, 
                       'Stressed' : 1
                     },
                   
                   "Satisfaction" : {
                       'Very Satisfied' : 5, 
                       'Satisfied' : 4, 
                       'Neutral' : 3, 
                       'Unsatisfied' : 2, 
                       'Very Unsatisfied' : 1 
                     },
                 
                    "Energy" : {'High' : 3, 'Medium' : 2, 'Low' : 1}
                 } 
    
    valid_day = len(MyData)

    # displayActivityDataSummary()
    calc_avgActivity(MyData, valid_day)


    TPI = TechProductivityIndex(MyData, valid_day)
    AAI = AcademicActivityIndex(MyData, valid_day)
    PHAI = PhysicalActivityIndex(MyData, valid_day)
    SRI = SleepRecoveryIndex(MyData, valid_day)
    ABI = ActivityBalanceIndex(MyData, valid_day)
    TUI = TimeUtilizationIndex(MyData, valid_day)
    EI = ExperienceIndex(MyData, experience, valid_day)
    DCI = DataContinuityIndex(valid_day, expectDays)

    PAI = PersonalActivityIndex(TPI, AAI, PHAI, SRI, TUI, EI, DCI)

    display(TPI, AAI, PHAI, SRI, ABI, TUI, EI, DCI, PAI)


# -------------------------Activity Data Summary--------------------------

# ========================================================================
#                             Average per Day
# ========================================================================



def getValue(value, activity):
    log = []

    for i in value:
        log.append(i[activity])
    return log

def calc_avgActivity(MyData, ValidDays):

    averageActivity = []

    avgSleep = sum(getValue(MyData, "sleep")) / ValidDays
    avgFitness = sum(getValue(MyData, "fitness")) / ValidDays
    avgStudy = sum(getValue(MyData, "study")) / ValidDays
    avgCoding = sum(getValue(MyData, "coding"))
    avgClass = sum(getValue(MyData, "class"))
    avgOtherActivity = sum(getValue(MyData, "otherActivity"))
    avgFreeTime = sum(getValue(MyData, "unaccounted"))

    # averageActivity.extend([
    #     ()avgSleep, avgFitness, avgStudy, avgCoding, avgClass, avgOtherActivity, avgFreeTime])

    # return averageActivity

# ------------------------------Index Value-------------------------------

# ========================================================================
#                   Total Productivity Index (TPI)
# ========================================================================

def TechProductivityIndex(data, validDays):

    coding = []

    for c_min in data:                      # This will acess each data in MyData list and
        coding.append(c_min['coding'])      # This will get the values one by one using ['keys']

    tpi = sum(coding) / validDays

    return tpi

# =========================================================================
#                       Academic Activity Index (AAI)
# =========================================================================

def AcademicActivityIndex(data, validDays):

    academic = []

    for acc in data:
        academic.append(acc['study'] + acc['class'])

    
    aai = sum(academic) / validDays

    return aai

# =========================================================================
#                       Physical Activity Index (PhAI)
# =========================================================================

def PhysicalActivityIndex(data, validDays):

    physicalActivity = []

    for phy in data:
        physicalActivity.append(phy['fitness'])

    phai = sum(physicalActivity) / validDays

    return phai

# =========================================================================
#                       Sleep & Recovery Index (SRI)
# =========================================================================

def SleepRecoveryIndex(data, validDays):

    sleepRecovery = []

    for slp in data:
        sleepRecovery.append(slp['sleep'])

    sri = sum(sleepRecovery) / validDays

    return sri

# =========================================================================
#                       Activity Balance index (ABI)
# =========================================================================

def ActivityBalanceIndex(data, validDays):
    unaccountedTime = []

    for ut in data:
        unaccountedTime.append(ut['unaccounted'])

    abi = sum(unaccountedTime) / validDays

    return abi

# =========================================================================
#                       Time Utilization Index (TUI)
# =========================================================================

def TimeUtilizationIndex(data, validDays):
    totalTrackedTime = []

    for tt in data:
        totalTrackedTime.append(tt['totalTrackedTime'])

    tui = sum(totalTrackedTime) / validDays

    return tui

# =========================================================================
#                       Experience Index (EI)
# =========================================================================

def ExperienceIndex(data, exp, validDays):
    experience = []

    for ex in data:
        f_text = ex["Feeling"]
        s_text = ex["Satisfaction"]
        e_text = ex["Energy"]

        f_value = exp["Feeling"][f_text]
        s_value = exp["Satisfaction"][s_text]
        e_value = exp["Energy"][e_text]

        experience.append(f_value + s_value + e_value)

    ei = sum(experience) / (validDays * 3)

    return ei

# =========================================================================
#                       Data Continuity Index (DCI)
# =========================================================================

def DataContinuityIndex(validDays, expectDays):
    dci = (validDays / expectDays) * 100

    return dci

# =========================================================================
#                       Personal Activity Index (PAI)
# =========================================================================

def PersonalActivityIndex(tpi, aai, phai, sri, tui, ei, dci):
    pai = (
              (0.15 * tpi ) 
            + (0.20 * aai ) 
            + (0.15 * phai) 
            + (0.20 * sri ) 
            + (0.15 * tui ) 
            + (0.10 * ei  ) 
            + ( 0.05 * dci)
          )
    return pai

# =========================================================================
#                               Display DATA
# =========================================================================

# def displayActivityDataSummary():
#     for activity in calc_avgActivity():



def display(TPI, AAI, PHAI, SRI, ABI, TUI, EI, DCI, PAI):
    print(f"Tech Productivity: {TPI:.2f} min / day")
    print(f"Academic Activity Index: {AAI:.2f} min / day")
    print(f"Physical Activity Index: {PHAI:.2f} min / day")
    print(f"Sleep Recovery Index : {SRI:.2f} min / day")
    print(f"Activity Balance index: : {ABI:.2f} min / day")
    print(f"Time Utilization index: : {TUI:.2f} min / day")
    print(f"Expering Index : {EI:.2f}")
    print(f"Data Continuity: {DCI:.2f} %")
    print(f"Personal Activity Index: {PAI:.2f}")


load_data("12607191.xlsx")