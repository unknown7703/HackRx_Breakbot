import json
import httpx
# book an appointment
def book_appointment()->str:
    """Use this function to book an appointment.

    Args:
        empty

    Returns:
        str: JSON present in response
    """
    #call api for booking
    response = httpx.get('https://21bbs0122-bajaj-fullstack.vercel.app/book')
    response_json=response.json()
    #load json into py
    reply=json.load(response_json)
    return {reply["message"]}

# cancel an appointment
def cancel_appointment()->str:
    """Use this function to cancel an appointment.

    Args:
        empty

    Returns:
        str: JSON present in response
    """
    #call api for cancelation
    response = httpx.get('https://21bbs0122-bajaj-fullstack.vercel.app/cancel')
    response_json=response.json()
    #load json into py
    reply=json.load(response_json)
    return {reply["message"]}