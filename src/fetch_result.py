import requests
import re


def get_result(exam, year, board, roll, reg):
    s = requests.Session()

    try:
        body = s.get('http://www.educationboardresults.gov.bd/index.php?err=103').text
    except:
        raise Exception("Website is down")
    augend_addend = re.findall(r'<td align=\"left\" valign=\"middle\">(\d+) \+ (\d+)</td>', body)[0]
    augend_addend = [int(i) for i in augend_addend]
    payload = {
        'sr': '3',
        'et': '0',
        'exam': exam,
        'year': year,
        'board': board,
        'roll': roll,
        'reg': reg,
        'value_s': str(sum(augend_addend)),
        'button2': 'Submit'
    }

    try:
        result = s.post('http://www.educationboardresults.gov.bd/result.php', data=payload).text
    except:
        raise Exception("Website is down")
    name = re.findall(r'<td width=\"39%\" align=\"left\" valign=\"middle\" bgcolor=\"#EEEEEE\">([\w\s\.]+)</td>',
                      result)
    courses = re.findall(r'<td align=\"left\" valign=\"middle\" bgcolor=\"#EEEEEE\">([\w\s\+\.,&\-]+)</td>', result)
    courses += re.findall(r'<td align=\"left\" valign=\"middle\" bgcolor=\"#DEE1E4\">([\w\s\+\.,&\-]+)</td>', result)

    try:
        courses = courses[13:]
    except:
        raise Exception('Something went wrong')
    _result = (name, courses, result)

    return _result
