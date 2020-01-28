
    let contacts = [];
    let projects = [];

    contacts.push({
        "id": "GitHub",
        "url": "https://github.com/estasney"
    });

    contacts.push({
        "id": "LinkedIn",
        "url": "https://www.linkedin.com/in/eric-stasney-965962108"
    });

    contacts.push({
        "id": "Kaggle",
        "url": "https://www.kaggle.com/estasney"
    });

    contacts.forEach((x) => {
        const targetElement = document.querySelector(`#${x.id}`);
        targetElement.addEventListener("click", (e) => {
            e.preventDefault();
            gtag('event', 'click', {
                 'event_category': 'link',
                 'event_label': x.id,
                 'value': 1
                });
        })
    });

    projects.forEach((x) => {
        const targetElement = document.querySelector(`#${x.id}`);
        targetElement.addEventListener("click", (e) => {
            e.preventDefault();
            gtag('event', 'click', {
                 'event_category': 'project',
                 'event_label': x.id,
                 'value': 1
                });
            window.open()
        })
    });

