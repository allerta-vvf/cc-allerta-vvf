from cat.mad_hatter.decorators import hook, tool
from cat.log import log
from cat.plugins.allerta_vvf.utils.client import api_request

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
  If the user ask anything about Allerta or AllertaVVF, try to reply with the information you know."""

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
    Input is the new availability.
    """
    availability = input.lower().strip()
    log.info(f"Availability: {availability}")

    if availability == "available" or availability == "disponibile":
        available = True
        msg = "Your availability has been updated to available"
    elif availability == "not available" or availability == "non disponibile":
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
def allertavvf_what_is_allerta(input, cat):
    """
    Reply to questions about what is AllertaVVF, also know as Allerta.
    Example: "What is AllertaVVF?", "Cosa è Allerta?"
    Input is None.
    """
    return ALLERTAVVF_EXPLANATION
