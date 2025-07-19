
### **Part 1: Core Knowledge Breakdown by Topic**

This is a structured review of the key concepts from your slide decks. Focus on understanding the **"why"** behind each concept.

#### **Module 1: The Foundations (Network Basics, Cryptography Basics)**

*   **Network Models:**
    *   **OSI vs. TCP/IP:** Know the layers. For an HD, don't just list them; explain the *purpose* of each layer (e.g., "The Network Layer is responsible for logical addressing and routing between different networks").
*   **Addressing:**
    *   Clearly distinguish between Physical (MAC), Logical (IP), and Port addresses. Know which layer each one operates at.
*   **Cryptography Fundamentals:**
    *   **Symmetric vs. Asymmetric Crypto:** This is critical.
        *   **Symmetric (AES, DES):** One shared key. **Pro:** Fast. **Con:** Key distribution is hard.
        *   **Asymmetric (RSA, ElGamal):** Public/private key pair. **Pro:** Solves key distribution. **Con:** Slow.
    *   **Hybrid Systems:** Understand that we use asymmetric crypto to securely exchange a symmetric session key, and then use the fast symmetric key to encrypt the actual data. This is the foundation of TLS, IPsec, etc.
    *   **Hashing & MACs:**
        *   **Hash (SHA, MD5):** Provides integrity. Know the key properties: pre-image resistance and collision resistance.
        *   **MAC (HMAC):** Provides integrity AND authenticity using a shared secret key.
    *   **Digital Signatures:** Provides integrity, authenticity, AND non-repudiation using a private key to sign and a public key to verify.

#### **Module 2: Securing the Layers**

*   **Link-Layer Security:**
    *   **Vulnerabilities:** Understand MAC Spoofing and ARP Poisoning at a deep level.
    *   **Wireless Evolution:** This is a perfect analysis topic.
        *   **WEP:** Fundamentally broken. Why? Short IVs, static key, weak integrity check (CRC-32).
        *   **WPA:** An intermediate fix using TKIP.
        *   **WPA2:** The standard for years. Uses strong AES encryption.
        *   **WPA3:** Why is it better? Provides "Forward Secrecy" meaning a compromised password doesn't allow decryption of past traffic. This is a key HD point.
    *   **Authentication:** PSK (for home) vs. 802.1X/EAP (for enterprise). Understand the components of 802.1X (Supplicant, Authenticator, Authentication Server).
*   **Internet-Layer Security:**
    *   **IP Header:** Know the key fields (Source/Dest IP, Protocol, TTL). Understand that the Source IP is not authenticated, leading to **IP Spoofing**.
    *   **IPsec:** This is a major topic.
        *   **AH vs. ESP:** AH provides integrity/authenticity for the *entire* packet. ESP provides confidentiality (encryption) for the payload and optional integrity.
        *   **Transport vs. Tunnel Mode:** Transport mode secures payload between two hosts. Tunnel mode encapsulates the *entire* IP packet in a new one, used for VPNs/gateways. Be able to draw or describe what is encrypted/authenticated in all four combinations (AH/Tunnel, ESP/Transport, etc.).
        *   **IKE (Internet Key Exchange):** The protocol that negotiates IPsec SAs.
            *   **Phase 1:** Creates a secure channel. Main Mode (6 messages, protects identity) vs. Aggressive Mode (3 messages, faster, exposes identity). This trade-off is a classic exam question.
            *   **Phase 2:** Negotiates the actual SAs to protect user data, operating inside the secure channel from Phase 1.
*   **Transport-Layer Security:**
    *   **TCP vs. UDP:** Reliability and connection-orientation (TCP) vs. speed and low overhead (UDP).
    *   **TLS (The successor to SSL):**
        *   **Purpose:** To secure TCP communications.
        *   **Handshake Protocol:** Understand the main steps: `ClientHello` (offering ciphersuites), `ServerHello` (choosing one), Server sends `Certificate`, Key Exchange occurs, `ChangeCipherSpec`, `Finished`.
        *   **Record Protocol:** This is what encrypts and authenticates the actual application data after the handshake is complete.
    *   **DTLS:** TLS for UDP. The key challenge it solves is packet loss. The main modification is adding a `HelloVerifyRequest` with a cookie to prevent DoS attacks.
    *   **QUIC:** The future. Built on UDP. **Key HD point:** It solves TCP's head-of-line blocking by using independent streams within a single connection. It also has a faster (0-RTT) handshake.
*   **Application-Layer Security:**
    *   **Email Security:** PGP vs S/MIME. The fundamental difference is the trust model. **PGP** uses a decentralized **Web of Trust**. **S/MIME** uses a centralized, hierarchical trust model with CAs (like TLS).
    *   **Kerberos:** Know the three "heads": Client, Authentication Server (AS), and Ticket-Granting Server (TGS). Understand the flow: 1. Get TGT from AS. 2. Use TGT to get a service ticket from TGS. 3. Use service ticket to access the end server. Understand the difference between a **Ticket** (for a server to decrypt) and an **Authenticator** (for a client to prove its identity).
    *   **SSH:** Composed of three protocols (Transport, Authentication, Connection). The Transport Layer Protocol uses a Diffie-Hellman key exchange to establish a secure channel. It's famous for **Port Forwarding** (tunneling insecure traffic through a secure SSH channel).

#### **Module 3: Overarching Security Concepts**

*   **Network Security Tools:**
    *   **Firewalls:** The workhorse. They filter traffic based on IP addresses, ports, and protocols. Understand Stateless (packet-by-packet) vs. Stateful (connection-aware) firewalls.
    *   **DMZ:** A buffer network between your internal network and the internet. Hosts publicly accessible services like web servers.
    *   **IDS vs. IPS:** An IDS *detects* and alerts. An IPS *prevents* by actively blocking traffic.
    *   **Signature vs. Anomaly Detection:** Signature detection looks for known patterns of attack (like an antivirus signature). Anomaly detection looks for deviations from a baseline of normal behavior.
*   **Post-Quantum Cryptography (PQC):**
    *   **The Threat:** Shor's algorithm (on a future quantum computer) will break all current public-key crypto (RSA, DH, ECC). Grover's algorithm weakens symmetric crypto (requiring us to double key lengths for AES, SHA).
    *   **The Problem:** The "store now, decrypt later" attack. An adversary can record your encrypted data today and wait for a quantum computer to exist to decrypt it.
    *   **The Solution:** PQC algorithms based on different mathematical problems (lattices, codes, etc.). NIST has standardized several: **CRYSTALS-Kyber** for key exchange and **CRYSTALS-Dilithium** for signatures.

---

### **Part 2: Exam Question Strategy**

**Multiple Choice (12 Qs, 24 marks)**

This section will test your breadth of knowledge. The 24 marks are nearly half the passing requirement, so it's vital.

*   **How to study:** Use flashcards for key terms, acronyms, and simple facts (e.g., "Which protocol uses a Web of Trust?" -> PGP; "What port does HTTPS use?" -> 443).
*   **During the exam:** Read carefully. Eliminate obviously wrong answers first. Watch out for absolutes like "always" or "never." If you are unsure, make an educated guess and move on. Don't spend too much time on a single 2-mark question.

**Short Answer & Protocol Analysis (11 Qs, 36 marks)**

This is where you earn your HD.

*   **"Explain/Describe" Questions:** Be precise and structured. Use bullet points. Define the term, state its purpose, and briefly explain how it works.
    *   *Example Question:* "Describe the purpose of the Ticket-Granting Ticket (TGT) in Kerberos."
    *   *HD Answer:* "The TGT's purpose is to allow a user to authenticate once to the Authentication Server (AS) and then request multiple service tickets from the Ticket-Granting Server (TGS) without re-entering their password. It acts as a temporary credential. The TGT is encrypted with the TGS's secret key, so the client cannot read it, but can present it to the TGS as proof that the AS has vouched for their identity."
*   **"Compare and Contrast" Questions:** Use a table if possible. Have clear criteria for comparison.
    *   *Example Question:* "Compare IPsec's Authentication Header (AH) and Encapsulating Security Payload (ESP)."

| Feature | Authentication Header (AH) | Encapsulating Security Payload (ESP) |
| :--- | :--- | :--- |
| **Confidentiality**| No (Plaintext data) | Yes (Encrypts payload) |
| **Integrity** | Yes | Yes (Optional but almost always used) |
| **Scope** | Authenticates the entire packet, including parts of the IP header. | Authenticates only the ESP header, payload, and trailer. |
| **Use Case** | When data confidentiality is not required, but authenticity is paramount. | The standard choice for VPNs as it provides both confidentiality and integrity. |
*   **"Analyze" Questions:** This requires you to show the pros and cons and come to a conclusion.
    *   *Example Question:* "Analyze the security of Kerberos V4's reliance on timestamps."
    *   *HD Answer:* "Kerberos V4 timestamps are a critical component for preventing replay attacks. The Authenticator contains a timestamp, and the server will only accept it if it is recent (e.g., within 5 minutes). **Strength:** This is a simple and effective defense against basic replay attacks where an attacker captures and resubmits a credential. **Weakness:** This creates a strict dependency on synchronized clocks across all clients and servers. If a client's clock is significantly skewed, authentication will fail, leading to a denial of service. Furthermore, a short validity window might still be vulnerable to very fast replay attacks within that window."

---

### **Part 3: Final Study Plan & Tips (Now until Sept 4th)**

You have plenty of time. A structured approach will prevent last-minute cramming.

1.  **Now - End of July (Deep Dive - Foundations):**
    *   Master the **Network Basics**, **Cryptography Basics**, and **CSCI368 Intro** slides. Make your own summary notes. Ensure you can explain the core concepts without looking at the slides.

2.  **August 1st - 15th (Deep Dive - Core Layers):**
    *   Tackle the big topics: **Link-Layer**, **Internet-Layer**, and **Transport-Layer**. Create the comparison tables mentioned above (WEP->WPA3, AH vs ESP, etc.). Draw the IPsec and TLS packet/handshake diagrams from memory.

3.  **August 16th - 25th (Deep Dive - Applications & Tools):**
    *   Focus on **Application-Layer**, **Network Security Tools**, and **PQC**. At this point, you should be actively trying to connect these topics to the lower layers you just studied.

4.  **August 26th - Sept 1st (Practice & Synthesis):**
    *   Go through all the question bank files (`PKI Exam Questions`, `CSCI368 Question Bank`, etc.). Don't just look at the answers; *write out your own answers* to the short-answer questions first, then compare them to the model answers. Identify your weak spots.
    *   **Self-Test:** Pick a protocol (e.g., IPsec VPN) and explain the entire security process from end-to-end, naming the protocols and technologies used at each layer.

5.  **Sept 2nd & 3rd (Final Review):**
    *   Read through your own summary notes. Review your comparison tables. Don't try to learn anything new. Relax. Get a good night's sleep before the exam.

**Final Exam Tip:** Answer the questions you know first to build confidence and secure marks. For the analysis questions, a good structure (e.g., Intro, Strengths, Weaknesses, Conclusion) can make your answer look much more professional and is more likely to get top marks. Good luck
