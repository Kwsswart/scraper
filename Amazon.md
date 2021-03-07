# End Objective Format per entry:

{
    {
        "nombre": "nombre de producto",
        "amazonURL": {
            "search": "https://www.amazon.es/s?k=<<palabraclave>>&i=<<categoria>>",
            "productPage": "https://www.amazon.es/<<unico>>/dp/<<unico>>" /"https://www.amazon.es/dp/B07Y8RH66Y/"

        }
        "descripcion": [],
        "precioRecommendado": "...",
        "precioActual": "...",
        "rating": "...",
        "numeroDeValores": "...",
        "valores": [{
            "nombre": "...",
            "rating": "...",
            "title": "...",
            "mensaje": "...",
            "fecha": "..."
        }],
        "datosTecnicos": {
            "marca": "...",
            "Fabricante": "...",
            "Series": "...",
            ....
        },
        "images": []
        }
    },
    .....
}

# Pseudocode:

Entry-point: https://www.amazon.es/s?k= << Key Word >> &i= <<Category>> &page= <<page number >> &language= <<Language code i.e. es en>>

1. in URL find_all <div class=" s-result-item">
    lists = []
    for each <div>:
        in <div> find <h2>
            in <h2> find <a>
                productpage = a["href"]
                in <a> get <span>
                    name = span.text.strip()
        list.append({'nombre':name, amazonURL: {
            'search': entryURL,
            'productPage': productpage
        }})

    return lists

2. Traverse list calling the productPage url and updating dictionary

    - for each dict in lists: // de below and return updated dictionary
        
        - in page find <div id="dp-container"> 
            - Set all variables before beginning in order to fill dict at the end and return it

            1. imgs: in <div id="dp-container"> find <div id="altImages"> func1()
                images = []
                - in <div> find_all <img tags>
                    for each <img>
                        images.append(img["src"])
                    return images

            2. Prices: in <div id="dp-container"> find <div id="price"> func2()
                - in <div id="price"> find <span id="priceblock_ourprice">
                    if <span> 
                        recommendedP = span.text.strip()
                        actualP = span.text.strip() 
                    else:
                        - in <div id="price"> find <span class="priceBlockStrikePriceString ">
                            recommendedP = span.text.strip()
                        - in <div> find <span id="priceblock_dealprice">
                            actualP = span.text.strip()

                    return {
                        "precioRecommendado": recommendedP,
                        "precioActual": actualP
                    }

            3. Ratings and reviews: // func3() & func4()
                - in <div id="dp-container"> find <div id="averageCustomerReviews">
                    - in <div id="averageCustomerReviews"> find <span id="acrCustomerReviewText">
                        numberReviews = span.text.strip()
                    - in <div id="averageCustomerReviews"> find <span class="a-icon-alt">
                        rating = span.text.strip()     
                    return {
                        "rating": rating,
                        "numeroDeValores": numberReviews,
                    }
                        
                - in <div id="dp-container"> find_all <div data-hook="review">
                    reviews = []
                    for each <div data-hook="review">
                        - in <div data-hook="review"> find <span data-hook="review-date">
                            date = span.text.strip()
                        - in <div data-hook="review"> find <i class="review-rating">
                            - in <i class="review-rating"> find <span>
                                rating = span.text.strip()
                        - in <div data-hook="review"> find <span class="review-title">
                            if <span class="review-title">:
                                in <span  class="review-title"> find <span class="cr-original-review-content">
                                    title = span.text.strip()
                            else:
                                in <div data-hook="review"> find <a class="review-title">
                                    in <a class="review-title"> find <span>
                                        if <span>
                                            title = span.text.strip()
                                        else:
                                            title = "Not Found"
                        - in <div data-hook="review"> find <div class="review-data">
                            - in <div class="review-data"> find <span class="cr-original-review-content">
                                message = span.text.strip()
                        - in <div  data-hook="review"> find <span class="a-profile-name">
                            name = span.text.strip()

                        review.append({
                            'nombre': name, 
                            'rating': rating, 
                            'title': title, 
                            'mensaje': message, 
                            'fecha': date})
                    return {"valores":reviews}

            4. Descripcion: func5()
                - in <div id="dp-container"> find <div id="feature-bullets">
                    description = []
                    - in <div id="feature-bullets"> find_all <span class="a-list-item">
                        for each <span class="a-list-item">:
                            description.append(span.text.strip())
                    return {
                        "decripcion": decription
                    }
                    
            5. Datos tecnicas: func6()
                - in <div id="dp-container"> find <table id="productDetails_techSpec_section_1">
                    header = []
                    data = []
                    - in <table id="productDetails_techSpec_section_1"> find all <tr>
                        - for each <tr>
                            - find <th>
                                header.append(th.text.strip())
                            - find <tr>
                                data.append(th.text.strip())
                    dictionary = dict()
                    for i in range(len(header) - 1):
                        dictionary.update({
                            header[i]: data[i]
                        }) 
                    return {
                        "datosTechnicos": dictionary  
                    }  

        6. Form final :
            choices = [func5(), func2(), func3(), func4(),func1()]
            for i in range(len(choices) - 1):
                dict.update(choices[i])
            return dict
        
3. Convert dictionary to json   
