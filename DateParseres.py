import datetime


def parse_date(date):
    date = date.split("/")
    m = date[1]
    # if(int(m)<10):
    #     m="0"+m
    d = date[0]
    y = date[2]
    return datetime.datetime.strptime(m + d + y, "%d%m%Y").date()


def parse_excel_date(date):
    date = date.split("/")
    m = date[1]
    # if(int(m)<10):
    #     m="0"+m
    d = date[0]
    if int(date[2]) > 80:
        y = "19"+date[2]
    else:
        y = "20" + date[2]
    return str(datetime.datetime.strptime(m + d + y, "%m%d%Y").date())


# def parse_date(date):
#     date = date.replace("  "," ").replace(" ","").upper()
#     return datetime.datetime.strptime(date, "%b%d%Y").date()


def parse_python_date_format(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()