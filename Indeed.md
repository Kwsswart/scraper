# End Objective Format per entry:

{
    {
        "nombre": "nombre de empresa",
        "indeedUrl": {
            "job": "url",
            company: "url"
        },
        "localidad": "...",
        "jobtitle": "...",
        "salario": "...",
        "rating" : "...",
        "descripcion": "...",
        "sitioweb": "..."
        "fecha": "timestampe/txt"
    }
    .....
}

# Pseudocode:

1. https://es.indeed.com/ofertas?q=<<key word search >>&l=<<location>>  
    - In page find_all <div class="jobsearch-SerpJobCard">
        jobs = []
        for each in <div>
            - In <div> for each company wanted find <h2 class="title">
                - In <h2> find <a>
                    title = a["title] 
                    job= a["href]
            - In <div> find <div class="jobsearch-SerpJobCard-footer">
                - in <div> find <span class="date">
                    - date = span.text.strip()
            - in <div> find <span class="company">
                - company = span.text.strip()
            - in <div> find <div class="recJobLoc">
                - location = div["data-rc-loc"]
            - in <div> find <div class="summary">
                - for <li> in <div>
                    summary(li.text.strip())
            - in <div> find <span class="salaryText">
                if not there: 
                    salary = "Not Found"
                else:
                    salary = span.text.strip()

            dictionary = {
                    nombre: company,
                    indeedURL: job,
                    localidad: location,
                    jobtitle: title, 
                    salario: salary,
                    descripcion: summary,
                    tiempo: date
                }
            jobs.append(dictionary)

2. Once in list of dictionaries convert to json.