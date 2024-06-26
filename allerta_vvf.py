from cat.mad_hatter.decorators import hook, tool
from cat.log import log
from cat.plugins.allerta_vvf.utils.client import api_request
import json
import urllib.parse

ALLERTAVVF_EXPLANATION = """AllertaVVF,
an unofficial open source firefighters' management software.
It can me abbreviated with "Allerta".
With this program, firefighters can do these things:
- Update their availability;
  if they are "available" they can be called in case of fire and other emergencies,
  else not. In Italian they refer to this function as "Disponibilità" or "Aggiornamento disponibilità"
  and they refer to available with "disponibile" and not available as "non disponibile".
- See other users availability
  They can see a list, with every user's name, surname and if they are available or not.
  If the user ask anything about Allerta or AllertaVVF, try to reply with the information you know.
- Read the last services
  In Italian they refer to this function as "Interventi" or "Ultimi interventi" or "Ultimi N interventi".
  In Italian, prefer saying "interventi" instead of "servizi".
  In every service, there are a chief and a list of drivers and a list of crew members.
"""

@hook
def agent_prompt_prefix(prefix, cat):
    # change the Cat's personality
    prefix = """You are an AI assistant for volunteer firefighters, and you can talk with an online platform:
"""+ALLERTAVVF_EXPLANATION+"""
You must reply in user's language, and you must be polite and helpful.
You must respect privacy and confidentiality.
You are NOT a cat. You are a virtual assistant for firefighters.
"""
    return prefix

@tool
def allertavvf_update_availability(input, cat):
    """
    Reply to questions about updating availability.
    Example: "Set my availability to available", "Set availability to not available",
    "Aggiorna la mia disponibilità a disponibile", "Aggiorna la disponibilità a non disponibile"
    Input should be the new availability, in the format "available" or "not available" or "None" if not clear from the sentence.
    If it's in other language, provide only one of that 3 options translating if necessary.
    """
    availability = input.lower().strip()
    log.info(f"Availability: {availability}")

    if availability == "available":
        available = True
        msg = "Your availability has been updated to available"
    elif availability == "not available":
        available = False
        msg = "Your availability has been updated to not available"
    else:
        return "I don't understand the availability you want to set"
    
    api_request(cat, "availability", "POST", {
        "available": available
    })
    
    return msg

@tool
def allertavvf_get_current_user_availability(input, cat):
    """
    Reply to questions about getting current user availability.
    You must reply with the current user availability, available or not available.
    Example: "What is my availability?", "La mia disponibilità?" "Sono disponibile?"
    Input is None.
    """
    response = api_request(cat, "availability")
    availability = "available" if response["available"] else "not available"
    return f"Your availability is {availability}"

@tool
def allertavvf_search_in_services(searchQueryText, cat):
    """
    Reply to user questions about retrieving services (or services data).
    You can use the following queries to search for services:
    - "last": get the last n of services
    - "from": filter services from a certain date
    - "to": filter services until a certain date
    The input is list of dictionaries with the query and the value, for example:
    [{"query": "last", "value": 5}] for the question "Get the last 5 services"
    [{"query": "from", "value": "2021-01-01"}] for the question "Get services data from 2021-01-01"
    [{"query": "to", "value": "2021-01-01"}] for the question "Leggi gli interventi fino al 2021-01-01"
    The user can ask to filter using multiple queries, for example:
    [{"query": "from", "value": "2021-01-01"}, {"query": "to", "value": "2021-01-31"}] for the question "Get services data from 2021-01-01 to 2021-01-31"
    This tool returns the JSON representation of the search queries.
    """

    try:
        data = json.loads(searchQueryText)
    except Exception as e:
        log.error(e)

    return searchQueryText

@tool
def allertavvf_retrieve_services_after_query_obtained(searchQueryText, cat):
    """
    Use this tool after the search_in_services tool to retrieve the services data.
    Input is the JSON response from the previous tool.
    Output is a JSON representation of the services data.
    Return them in a human readable format, especially dates.
    If there are no services, return "No services found".
    """
    response = api_request(cat, "services/?query="+urllib.parse.quote(searchQueryText)+"&external")

    return json.dumps(response, ensure_ascii=False)

@tool
def allertavvf_what_is_allerta(input, cat):
    """
    Reply to questions about what is AllertaVVF, also know as Allerta.
    Example: "What is AllertaVVF?", "Cosa è Allerta?"
    Input is None.
    """
    return ALLERTAVVF_EXPLANATION
