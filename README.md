# HackRx_Breakbot

## Requested Features (Title WIP)
- List of all the things that they asked for and we have implemented the same

## Major Features
- These will get screenshots and stuff
- Created an Admin UI for easily uploading PDFs and keeping the knowledge base up to date

## Additional Features
- Use can upload files and we can add them to the context
- even in the admin side people can upload handwritten files, even user can upload handwritten files
- can do some sort of intent mapping as well, if the user is showing a certain type of itent then we can flag it in the backend (lvl 1)
- we can followup on the lead in the

### TODO

- Having screenshots/gifs of specific usecases that we serve will be pretty useful imo
    - Like handling FAQS
    - Escalation Handling (For e.g. if a user is having a lot of problems then a tool call should be create a ticket and send an email to the user as well)
- For upload we should be able to handle:
    - need to allow batch upload and it should be able to identify the file type based on the extension
    - PDFs
    - PPTs
    - docx
    - support for txt file as well
    - even an external db (need to see how to do this -> We can probably just query the complete db and convert that into embeddings) 
- Need to do some sort of validation, like get the name of the pdf to make sure that it is not uploaded twice or something like that. (need to mention this in the README)

- Need to add a parameter in the api to let the user enter the format of the file
- all of this will be moved to a admin ui panel (need to discuss with aatreya)
- need to implement that python library that allows us to break code into modules
- in the case we end up coming first place, we should add it to the repository so people can come in the future and get all the context that they require
- need to create a section from additonal technological sanitations things that we are doing
    - like testing
    - like adding a reverse proxy with nginx
    - deployment using docker and things like that
    - added proper logging (need to research on this)
    - add a linter and make sure all the functions have a docstring in them
    - have to add type validation to all functions
    - have to mention that I have broken everything into classes so that if makes sense that we are following OOPS
    - can move everything to a class based format, so that some things happen at the initialization and we just have to call the function
    - Have to do appropriate twy-catch wherever possible
    - have to remove unnecessary import wherever possible
    - Can add GitHub actions to make sure code quality does not reduce
    - Use pydantic wherever possible
    - have to mention that we have used groq since it is the fastest
    - other things that we do are use Instructor and LLM guard
- Have to clean up requirement.txt as well

### When doing the ChatAPI validation
- Need to make sure it is only picking up from the context (add this to readme if we end up doing this in the Additional Features section)
- Need to try it to 

