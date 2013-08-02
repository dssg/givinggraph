import requests
import givinggraph.config
from collections import namedtuple

Nonprofit = namedtuple('Nonprofit', 'ein name impact financials people guidestar_org_id')
Person = namedtuple('Person', 'firstname middlename lastname title compensation')
Financials = namedtuple('Financials', 'total_revenue total_assets program_expenses admin_expenses \
    fundraising_expenses total_expenses funding_source')


# returns Person namedtuple if the response is OK, returns None is the response is not OK
def get_nonprofit(organization_id):
    url = 'https://data.guidestar.org/v1/commondata/' + organization_id + '.json'

    user = givinggraph.config.read_config('guide_star', 'user')
    password = givinggraph.config.read_config('guide_star', 'pass')
    r = requests.get(url, auth=(user, password))

    if r.status_code == 200:
        nonprofit_dict = r.json()
        name = nonprofit_dict['primary_organization_name']
        impact = nonprofit_dict['impact_statement']
        guidestar_org_id = nonprofit_dict['organization_id']

        # get financial info
        financials = nonprofit_dict['financials'][0]
        total_revenue = financials['total_revenue']
        total_assets = financials['total_assets']
        program_expenses = financials['program_expenses']
        admin_expenses = financials['administration_expenses']
        fundraising_expenses = financials['fundraising_expenses']
        fundraising_expenses = financials['fundraising_expenses']
        total_expenses = financials['total_expenses']
        funding_source = financials['funding_source']
        financials = Financials(total_revenue, total_assets, program_expenses, admin_expenses,
                                fundraising_expenses, total_expenses, funding_source)

        # get employee info
        people_list = r.json()['people']
        people = []
        for person_dict in people_list:
            firstname = person_dict['firstname']
            middlename = person_dict['middlename']
            lastname = person_dict['lastname']
            title = person_dict['title']
            compensation = person_dict['compensation']
            person = Person(firstname, middlename, lastname, title, compensation)
            people.append(person)

        return Nonprofit(ein, name, impact, financials, people, guidestar_org_id)
    else:
        return None
