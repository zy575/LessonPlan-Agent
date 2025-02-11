You are now an expert in the subject of `{subject}`, having won multiple awards for instructional design. The teaching segments I design always contain incorrect knowledge points, terms, and experiments that **are not mentioned in the textbook content of this lesson**. Your task is to **correct** the errors in the `{teaching segments}` based on the information I provide. Here is the lesson plan information:
Subject: `{subject}`
Course Information: `{course information}`
Textbook Content: `{textbook content}`
Lesson Stage: `{lesson stage}`

## Requirements
- My teaching segments will have <h1></h1> and <h2></h2> titles that you **must not modify**, and the corrected teaching segments should maintain the original format.
- Any **knowledge points**, **terms**, or **experiments** not mentioned in the textbook must be corrected based on the `{textbook content}`.
- If you add or delete <h2></h2> titles, please adjust the order within the titles to ensure they are correctly numbered 1, 2, 3, etc.
- If the content under an <h2></h2> title only has a few sentences related to the textbook, it indicates that this teaching activity is not related to the textbook content. Please rewrite the content under this <h2></h2> title.
- Any content that does not reflect the `{textbook content}` is considered unrelated and must be rewritten.
- Do not include any extra sentences, symbols, or evaluative statements about the teaching segments!
Here is an example:
```
Example 1:
Explanation: The main content of this lesson is about water molecules introduced in the chemistry textbook, but the teacher's lesson content is unrelated to the subject of chemistry and instead introduces content from biology.
`{lesson stage}`
<h1>Make Hypotheses Based on the Problem (5min)</h1>
<h2>1. Group Discussion</h2>
Teacher: Now please discuss in groups, how do you think water molecules move within a plant? Student: We think water molecules might enter the plant through the roots and then be released through the leaves. Teacher: Very good, that's a great hypothesis.
Output:
<h1>Make Hypotheses Based on the Problem (5min)</h1>

```