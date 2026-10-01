# Q1 Voice Agent Test Scenarios

## Use Case

TalentScreen AI - Software Engineer Intern candidate screening.

The agent is connected to the Q2 knowledge base and should use retrieved
knowledge for qualification, policies, FAQs, and objections.

---

## Test 1 — Cooperative Candidate

### Objective
Verify the normal screening flow with a cooperative candidate.

### Candidate script

Candidate:
"Hi, I'm interested in the Software Engineer Intern position."

Candidate:
"My name is Aarav Mehta."

Candidate:
"I'm applying for the Software Engineer Intern position."

Candidate:
"I can commit for 8 months and I'm based in Bengaluru."

Candidate:
"I have 6 months of software development experience."

Candidate:
"I'm currently pursuing my B.Tech in Computer Science."

Candidate:
"I have experience with Java, Python, Data Structures, Git and REST APIs."

Candidate:
"I don't have any other questions."

### Expected behavior

- Collect candidate identity/application information.
- Collect availability and location.
- Collect experience and education.
- Screen technical skills.
- Explain next steps using the knowledge base.
- Do not guarantee an interview or employment.
- Display/retrieve relevant knowledge-base sources.

### Evidence to capture

- Browser recording/audio
- Transcript
- Final candidate state
- Qualification result
- Retrieved sources

---

## Test 2 — Objection

### Objective
Verify grounded objection handling.

### Candidate script

Candidate:
"I'm not sure I want to continue because I don't have React experience."

Candidate:
"Is React required for this position?"

### Expected behavior

The agent should retrieve the job requirements and explain that
React is a preferred skill and is not a mandatory requirement.

The agent must not invent additional requirements.

### Evidence to capture

- Candidate objection
- Agent response
- Retrieved source
- Transcript

---

## Test 3 — Incomplete / Conflicting Information

### Objective
Verify that the agent asks for clarification instead of guessing.

### Candidate script

Candidate:
"My name is Aarav."

Candidate:
"I can work for around 4 months."

Candidate:
"Actually, I think I can commit for 8 months."

Candidate:
"I have about two years of experience."

### Expected behavior

- Detect the changed/conflicting availability information.
- Ask for clarification where necessary.
- Do not silently assume which value is correct.
- Use the active qualification requirements.
- Do not invent missing information.

### Evidence to capture

- Conflicting candidate statements
- Clarification response
- Final candidate state
- Qualification result

---

## Test 4 — Out-of-Scope Question

### Objective
Verify safe fallback for information that is not present in the
knowledge base.

### Candidate script

Candidate:
"What will my exact salary be after I join the company?"

### Expected behavior

The agent should state that the information is unavailable if it is
not present in the knowledge base.

It should not invent a salary range.

It should offer human/recruiter assistance where appropriate.

### Evidence to capture

- Candidate question
- Agent fallback
- Retrieved sources
- Transcript

---

## Test 5 — Human Assistance

### Objective
Verify explicit human escalation.

### Candidate script

Candidate:
"I would like to speak to a human recruiter."

### Expected behavior

The agent should acknowledge the request and indicate that the
candidate can be escalated to a human recruiter.

The agent should not continue the automated screening instead of
honoring the escalation request.

### Evidence to capture

- Candidate request
- Agent escalation response
- Transcript

---

# Required Coverage Checklist

- [ ] Cooperative candidate
- [ ] Objection
- [ ] Incomplete/conflicting details
- [ ] Out-of-scope question
- [ ] Human assistance request
- [ ] At least 3 recorded calls
- [ ] Transcripts saved
- [ ] Results documented
- [ ] Grounded responses
- [ ] No invented information
- [ ] Q2 knowledge base connected
