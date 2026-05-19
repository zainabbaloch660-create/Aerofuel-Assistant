import re

# Dictionary of questions and answers about aircraft refueling supervision
qa_pairs = {
    r"what is aircraft refueling supervision": "Aircraft refueling supervision involves overseeing the safe and efficient refueling of aircraft. Supervisors ensure compliance with safety protocols, verify fuel types and quantities, and coordinate with ground crews to prevent accidents.",
    r"what does an aircraft refueling supervisor do": "An aircraft refueling supervisor monitors the refueling process, checks equipment, ensures proper grounding of the aircraft, verifies fuel quality, and maintains safety standards to prevent fires or explosions.",
    r"what are the safety procedures": "Safety procedures include: grounding the aircraft, prohibiting smoking and open flames, wearing appropriate PPE, checking for fuel leaks, and ensuring proper ventilation. Supervisors must also be aware of weather conditions and emergency protocols.",
    r"what fuel is used": "Aircraft typically use Jet A or Jet A-1 fuel, which are kerosene-based. Supervisors must ensure the correct fuel type is used for the specific aircraft model.",
    r"how is refueling done": "Refueling is done through designated ports on the aircraft wings or fuselage. Supervisors oversee the connection of hoses, monitor fuel flow, and ensure the correct amount is dispensed without overfilling.",
    r"what qualifications are needed": "Qualifications include training in aviation safety, fuel handling, emergency response, and often certifications from aviation authorities. Experience in ground operations is beneficial.",
    r"what are common risks": "Common risks include fuel spills, electrostatic discharge, contamination, and human error. Supervisors mitigate these through strict adherence to procedures and regular equipment checks.",
    r"tell me about your profession": "As an aircraft refueling supervisor, my role is critical in aviation operations. I ensure that aircraft are safely fueled, maintaining the highest safety standards to protect lives and equipment.",
    r"what is the process": "The process involves: pre-refueling checks, connecting fuel lines, monitoring the transfer, post-refueling inspections, and documentation. Everything is done under supervision to ensure accuracy and safety.",
    r"why is supervision important": "Supervision is important to prevent accidents, ensure regulatory compliance, and maintain operational efficiency. It protects the aircraft, crew, and ground personnel from hazards associated with fuel handling."
}

def get_response(user_input):
    user_input = user_input.lower()
    for pattern, response in qa_pairs.items():
        if re.search(pattern, user_input):
            return response
    return "I'm sorry, I don't have information on that. Can you ask about aircraft refueling supervision?"

def main():
    print("Welcome to AeroFuel Assistant!")
    print("Ask one question at a time. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("AeroFuel Assistant: Goodbye!")
            break
        response = get_response(user_input)
        print(f"AeroFuel Assistant: {response}")

if __name__ == "__main__":
    main()