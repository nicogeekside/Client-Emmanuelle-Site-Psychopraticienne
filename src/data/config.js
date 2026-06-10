export const siteInfo = {
    name: "Emmanuelle Demeulemeester",
    shortName: "Emmanuelle",
    title: "Psychopraticienne à Saint-Nazaire | EMDR & EFT",
    phone: "07 67 15 84 71",
    email: "contact@emma-psychopraticienne.fr",
    address: {
        street: "7 rue de l'étoile du matin",
        city: "Saint-Nazaire",
        zip: "44600",
        full: "7 rue de l'étoile du matin, 44600 Saint-Nazaire",
        region: "Loire-Atlantique",
        country: "FR"
    },
    siret: "989 070 727 00015",
    geo: {
        latitude: "47.2735",
        longitude: "-2.2010"
    }
};

export const navItems = [
    { name: 'Accueil', href: '/' },
    { name: 'Qui suis-je ?', href: '/a-propos-emmanuelle/' },
    { name: 'Blog', href: '/blog/' },
];

export const navDropdownFormats = {
    label: 'Lieux de consultation',
    items: [
        { name: 'En cabinet', href: '/therapie-cabinet-saint-nazaire/' },
        { name: 'En visio', href: '/therapie-en-ligne-visio/' },
        { name: 'En marchant', href: '/therapie-en-marchant-saint-nazaire/' },
        { name: 'Post-Partum', href: '/espace-soutien-post-partum/' },
    ]
};

export const navDropdown = {
    label: 'Mes approches',
    items: [
        { name: 'Thérapie EMDR', href: '/therapie-emdr-saint-nazaire/' },
        { name: 'Séances EFT', href: '/seance-eft-gestion-emotions/' },
    ]
};

export const formats = [
    {
        id: "marchant",
        icon: "🚶‍♀️",
        title: "Thérapie en marchant",
        subtitle: "Thérapie en mouvement",
        description: "Marchez à mes côtés et laissez la parole venir naturellement. Côte à côte, en mouvement, certaines choses se disent plus facilement. Une approche douce et libératrice.",
        note: "Séances en plein air, à votre rythme",
        href: "/therapie-en-marchant-saint-nazaire/",
        color: "from-emerald-50 to-emerald-100/50",
        accent: "text-emerald-800",
        border: "border-emerald-200"
    },
    {
        id: "visio",
        icon: "💻",
        title: "Thérapie en visio",
        subtitle: "Depuis chez vous",
        description: "Bénéficiez du même accompagnement de qualité depuis le confort de votre domicile, partout en France. Flexible, confidentiel et efficace.",
        note: "Disponible partout en France",
        href: "/therapie-en-ligne-visio/",
        color: "from-blue-50 to-indigo-50/50",
        accent: "text-blue-800",
        border: "border-blue-200"
    },
    {
        id: "cabinet",
        icon: "🛋️",
        title: "Thérapie en cabinet",
        subtitle: "Un espace sécurisant",
        description: "Venez dans mon cabinet apaisant à Saint-Nazaire. Un cadre chaleureux et confidentiel pensé pour que vous vous sentiez en sécurité dès la première seconde.",
        note: "Saint-Nazaire — Parking gratuit",
        href: "/therapie-cabinet-saint-nazaire/",
        color: "from-rose-50 to-orange-50/50",
        accent: "text-rose-800",
        border: "border-rose-200"
    },
    {
        id: "post-partum",
        icon: "🤱",
        title: "Espace Post-Partum",
        subtitle: "Rassemblement mensuel",
        description: "Un espace de parole bienveillant et sans jugement, ouvert aux mamans et aux papas. Pour traverser ensemble les bouleversements de la parentalité.",
        note: "Groupe mensuel — Hommes & Femmes",
        href: "/espace-soutien-post-partum/",
        color: "from-purple-50 to-fuchsia-50/50",
        accent: "text-purple-800",
        border: "border-purple-200"
    }
];

export const epreuves = [
    "Traumatismes", "Deuil", "Anxiété", "Périnatalité",
    "Phobies", "Stress", "Confiance en soi", "Douleurs chroniques",
    "Post-Partum", "Burn-out", "Trouble du sommeil", "Séparation"
];

export const reviews = [
    {
        name: "Karine S.",
        text: "Emmanuelle est une thérapeute très professionnelle, bienveillante et à l'écoute. Grâce à son expertise en EFT, elle m'a aidée à traverser des situations émotionnellement difficiles avec plus de sérénité. Je la recommande à 100 % !",
        stars: 5,
        tag: "EFT"
    },
    {
        name: "Mumu Shahata",
        text: "Excellente professionnelle ! Le cabinet est chaleureux, apaisant et très agréable. Emmanuelle Demeulemeester est à l'écoute, bienveillante et offre un accompagnement de grande qualité. Je me suis sentie en confiance dès la première séance. Je recommande vivement !",
        stars: 5,
        tag: "Accompagnement"
    },
    {
        name: "viaud Stephane Nathalie",
        text: "Merci Emmanuelle pour cette découverte de l'EFT. Votre accueil et vos paroles m'ont permis de me sentir en confiance. J'ai apprécié cette séance qui m'a permis d'être détendue. Merci pour votre professionnalisme et très belle continuation.",
        stars: 5,
        tag: "EFT"
    },
    {
        name: "tyhia angama",
        text: "Première séance d'EMDR avec Emmanuelle. Elle a été très douce et rassurante. Elle a bien expliqué chaque étape, ce qui m'a permis de me sentir en confiance. J'ai eu l'impression d'avancer dès cette première consultation. Le cabinet est calme, propre et très agréable. Je recommande vraiment.",
        stars: 5,
        tag: "EMDR"
    },
    {
        name: "Le Berre Valerie",
        text: "Je recommande cette thérapeute qui m'a permis d'avancer dans ma vie ... je me sentais bloquée et jai compris que c'était lié a des événements du passé que je n'arrivais pas a digérer... la technique EFT est assez bluffante, très douce et en même temps super efficace. Un chaleureux merci. Je recommande sans hésitation.",
        stars: 5,
        tag: "EFT"
    }
];
