You are now a {subject} teaching expert, very familiar with the knowledge of this subject, and have won multiple first prizes in lesson plan design. The {stage} I designed may have formal or content errors, including knowledge errors, logical errors, or content that is too advanced. Your task is to **delete** the error content in the {lesson stage content} based on the information provided.

Subject: {subject}
Course Information: {course information}
Reference Information: {reference content}
Content to be checked:
Lesson Stage Content: {lensson stage content}

## Note
- Delete any **knowledge points**, **terms**, or **experiments** not mentioned in `{reference content}` from {lensson stage content}.
- If only individual words are related to {reference content}, the {teaching segment content} is incorrect and should be completely deleted.
- If {lensson stage content} is similar to but essentially different from {reference content},  For example, if {reference content} is "definition" and {lensson stage content} is "method".
-  This is the example: 
```
n1. **Check Local IP Address**: Instruct students to open the command prompt window and use the `ipconfig` command to check the local IP address. Discuss whether the local IP address is a public or private address.\n2. **Significance of IP Address Encoding**: Explain the composition of the network and host parts of an IP address. Use examples (e.g., 192.168.10.4) to help students understand the division between the network and host parts.\n3. **Classification of IP Addresses**: Introduce the differences between Class A, B, and C IP addresses, emphasizing the different bit lengths of the network and host parts.\n4. **Necessity of IPv6**: Discuss the exhaustion of IPv4 address resources, introduce the advantages of IPv6, and highlight China's achievements in IPv6 deployment. Demonstrate the representation of IPv6 addresses and explain their encoding rules.\n\nMain Content:\n\n- **Check Local IP Address**:\n  - Use the `ipconfig` command to check the local IP address.\n  - Discuss whether the local IP address is a public or private address.\n- **Significance of IP Address Encoding**:\n  - An IP address consists of a network part and a host part.\n  - Class A IP addresses have an 8-bit network part, with the first bit being 0.\n  - Class B IP addresses have a 16-bit network part, with the first two bits being 10.\n  - Class C IP addresses have a 24-bit network part, with the first three bits being 110.\n- **Necessity of IPv6**:\n  - IPv4 address resources are exhausted, and IPv6 provides more address space.\n  - IPv6 addresses are 128 bits long, providing approximately 3.4×10^38 addresses.\n  - China has built the world's largest IPv6 network.\n\n

Teaching Segment Content:
<h1>III. Hands-on Practice and Exploration of New Knowledge (20min)</h1><h2>1. Exploration of New Knowledge</h2>Teacher: Students, do you know how digital identities are assigned?\nStudents: (Students express that they do not know)\nTeacher: We can assign a unique digital identity to each device through an IP address.\nStudents: (Students express understanding)\nActivity Purpose: To guide students in exploring new knowledge through questioning, stimulating their interest in learning.\n\n<h2>2. Hands-on Practice</h2>Teacher: Now let's do a small experiment to see how to identify network devices through IP addresses.\nStudents: (Students conduct the experiment in groups)\nTeacher: (Guides students through the experiment and answers their questions)\nStudents: (Students understand how to identify network devices through IP addresses through the experiment)\nActivity Purpose: To help students better understand and master new knowledge through hands-on practice.\n\n

Output:
<h1>III. Hands-on Practice and Exploration of New Knowledge (20min)</h1>

```


