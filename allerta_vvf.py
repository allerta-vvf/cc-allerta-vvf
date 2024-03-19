from cat.mad_hatter.decorators import hook, tool
from cat.log import log
from cat.plugins.allerta_vvf.utils.client import api_request
import json

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
def allertavvf_get_last_n_service(input, cat):
    """
    Reply to questions about getting or summarizing the last service or the last N services.
    You must reply with the last service or the last N services, using the provided JSON data.
    Example: "What is the last service?", "Ultimo intervento", "Ultimi 5 servizi" "Ottieni gli ultimi 3 interventi" "Riassumi l'ultimo intervento".
    Reply in the language the user asked (if answer is in Italian, reply in Italian, if answer is in English, reply in English).
    For each service, say at least the name of the chief if user asked to summarize the service.
    Transform the date into an human readable format.
    Input is the number of services to return, or 1 if the user wants the last service.
    """
    try:
        n = int(input)
    except ValueError:
        n = 1
    response = api_request(cat, "services/last/"+str(n))

    keys_to_remove = [
        "id", "chief_id", "place_id", "type_id",
        "created_at", "added_by_id",
        "updated_at", "updated_by_id",
        "deleted_at", "deleted_by_id"
    ]
    for service in response:
        for key in keys_to_remove:
            service.pop(key, None)
        place = service["place"]["display_name"]
        service["place"] = place
        for d in service["drivers"]:
            d.pop("pivot", None)
        for c in service["crew"]:
            c.pop("pivot", None)
    response = json.dumps(response, ensure_ascii=False)
    return response

@tool
def allertavvf_what_is_allerta(input, cat):
    """
    Reply to questions about what is AllertaVVF, also know as Allerta.
    Example: "What is AllertaVVF?", "Cosa è Allerta?"
    Input is None.
    """
    return ALLERTAVVF_EXPLANATION
