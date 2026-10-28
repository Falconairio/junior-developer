export type Question = {
    category: string
    question: string
    sources: Source[]
    content: string
}

export type Source = {
    id: string
    title: string
    source: string
    icon: string
}
