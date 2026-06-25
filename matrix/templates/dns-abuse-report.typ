#set page(
  paper: "us-letter",
  flipped: true,
  margin: (left: 0.45in, right: 0.45in, top: 0.7in, bottom: 0.55in),
  header: image("matrix/assets/header.png", width: 100%),
  footer: context align(center)[
    #text(size: 7pt, fill: rgb("#555555"))[
      DNS Abuse Techniques Matrix - Page #counter(page).display("1")
    ]
  ],
)

#set text(font: "Arial", size: 8pt, lang: "en")
#set par(justify: true, leading: 0.55em)
#set heading(numbering: none)
#set table(
  stroke: 0.35pt + rgb("#c9d1d9"),
  inset: 2pt,
)

#show heading.where(level: 1): it => {
  set text(size: 20pt, weight: "bold", fill: rgb("#006b35"))
  block(above: 0pt, below: 6pt, it.body)
}

#show heading.where(level: 2): it => {
  set text(size: 13pt, weight: "bold", fill: rgb("#006b35"))
  block(above: 10pt, below: 4pt, it.body)
}

#show heading.where(level: 3): it => {
  set text(size: 10pt, weight: "bold", fill: rgb("#333333"))
  block(above: 7pt, below: 3pt, it.body)
}

#show link: set text(fill: rgb("#005ea8"))
$if(title)$
#align(center)[
  #text(size: 24pt, weight: "bold", fill: rgb("#006b35"))[$title$]
  $if(subtitle)$
  #linebreak()
  #text(size: 13pt, fill: rgb("#333333"))[$subtitle$]
  $endif$
  $if(website)$
  #linebreak()
  #text(size: 8.5pt)[#link("$website$")[$website$]]
  $endif$
]

#v(0.15in)
$endif$

$body$
