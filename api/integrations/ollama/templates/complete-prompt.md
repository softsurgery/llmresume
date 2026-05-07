{prompt}

Your task: generate a CV in JSON format compatible with RenderCV. Follow these rules exactly:

1. Return **only valid JSON**. Do NOT include any text, markdown, or backticks.
2. Use this structure:

{
"cv": {
"name": "string",
"location": "string",
"email": "string",
"website": "string (must start with http:// or https://)",
"social_networks": [{"network":"string","username":"string"}],
"sections": {
"summary": ["string"],
"education": [{"institution":"string","area":"string","degree":"string","start_date":"YYYY-MM-DD or YYYY-MM or YYYY","end_date":"YYYY-MM-DD or YYYY-MM or YYYY or 'present'","highlights":["string"]}],
"experience": [{"company":"string","position":"string","start_date":"YYYY-MM-DD or YYYY-MM or YYYY","end_date":"YYYY-MM-DD or YYYY-MM or YYYY or 'present'","highlights":["string"]}],
"projects": [{"name":"string","date":"YYYY-MM-DD or YYYY-MM or YYYY","highlights":["string"]}]
}
},
"design": {"theme":"string"} # must be top-level
}

3. Always use **full URLs** starting with http:// or https://
4. All date fields must use **YYYY-MM-DD, YYYY-MM, or YYYY**, or `"present"` for ongoing positions.
5. All section entries must be **lists**, even if empty.
6. Do not put `design` inside `cv.sections`; it must be at the top level.
7. Make sure all braces `{}` and brackets `[]` are correctly opened and closed.
8. For cv.social_networks, only use the following network names: LinkedIn, GitHub, GitLab, IMDB, Instagram, ORCID, Mastodon, StackOverflow, ResearchGate, YouTube,Google Scholar, Telegram, WhatsApp, Leetcode, X, Bluesky.
9. Try to avoid using many social networks unless specifically requested or provided by the user.
   - All other networks: free-form username string
10. If the user did not provide a username in the input, use a placeholder in the correct format:

- IMDB → "nm0000001"
- ORCID → "0000-0000-0000-0000"
- Mastodon → "@user@example.com"
- StackOverflow → "12345/username"

11. Do NOT invent invalid usernames. Always respect the required format.
    Do NOT use any other names. If the user mentions other networks, ignore them.
12. Aim for longer sentences and paragraphs.
13. theme must be one of: "classic", "ember", "engineeringclassic", "engineeringresumes", "harvard", "ink", "moderncv", "opal", "sb2nov".

Respond **only with valid JSON** following these rules.
