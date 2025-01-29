import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize Dash App with CDN stylesheets
app = dash.Dash(__name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
        "https://cdn.jsdelivr.net/npm/daisyui@3.9.4/dist/full.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    ]
)

# Islamic Books Dataset with Icons
books_data = [
    {
        "id": 1,
        "title": "The Noble Quran",
        "author": "Allah (Revealed to Prophet Muhammad)",
        "category": "Holy Book",
        "description": "The central religious text of Islam",
        "icon": "fas fa-book-quran",
        "text_color": "text-green-600",
        "bg_color": "bg-green-100",
        "rating": 5.0
    },
    {
        "id": 2,
        "title": "Sahih Al-Bukhari",
        "author": "Imam Al-Bukhari",
        "category": "Hadith",
        "description": "Most authentic hadith collection",
        "icon": "fas fa-scroll",
        "text_color": "text-blue-600",
        "bg_color": "bg-blue-100",
        "rating": 4.9
    },
    {
        "id": 3,
        "title": "Riyad us-Saliheen",
        "author": "Imam An-Nawawi",
        "category": "Islamic Teachings",
        "description": "Gardens of the Righteous",
        "icon": "fas fa-mosque",
        "text_color": "text-red-600",
        "bg_color": "bg-red-100",
        "rating": 4.7
    }
]

# Create DataFrame
df_books = pd.DataFrame(books_data)

# Navbar Component
def create_navbar():
    return html.Div(
        className="navbar bg-green-500 text-white shadow-lg",
        children=[
            html.Div(
                className="navbar-start",
                children=[
                    html.A(
                        className="btn btn-ghost normal-case text-xl",
                        children=[
                            html.I(className="fas fa-library mr-2"),
                            "Islamic Library"
                        ]
                    )
                ]
            ),
            html.Div(
                className="navbar-center hidden lg:flex",
                children=[
                    html.Ul(
                        className="menu menu-horizontal px-1",
                        children=[
                            html.Li(html.A([
                                html.I(className="fas fa-home mr-1"),
                                "Home"
                            ], href="/", className="text-white hover:bg-green-600")),
                            html.Li(html.A([
                                html.I(className="fas fa-book mr-1"),
                                "Books"
                            ], href="/books", className="text-white hover:bg-green-600")),
                            html.Li(html.A([
                                html.I(className="fas fa-tags mr-1"),
                                "Categories"
                            ], href="/categories", className="text-white hover:bg-green-600"))
                        ]
                    )
                ]
            ),
            html.Div(
                className="navbar-end",
                children=[
                    html.A(
                        className="btn bg-blue-500 text-white hover:bg-blue-600",
                        children=[
                            html.I(className="fas fa-search mr-1"),
                            "Search"
                        ]
                    )
                ]
            )
        ]
    )

# Book Card Component
def create_book_card(book):
    return html.Div(
        className=f"card w-96 {book['bg_color']} shadow-xl",
        children=[
            html.Div(
                className="px-10 pt-10",
                children=[
                    html.I(
                        className=f"{book['icon']} text-6xl {book['text_color']}"
                    )
                ]
            ),
            html.Div(
                className="card-body items-center text-center",
                children=[
                    html.H2(
                        className=f"card-title {book['text_color']}",
                        children=book['title']
                    ),
                    html.P(f"Author: {book['author']}"),
                    html.P(f"Category: {book['category']}"),
                    html.Div(
                        className="card-actions",
                        children=[
                            html.Div(
                                className="badge bg-red-500 text-white",
                                children=[
                                    html.I(className="fas fa-star mr-1"),
                                    f"Rating: {book['rating']}/5"
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

# App Layout
app.layout = html.Div(
    className="min-h-screen bg-green-50",
    children=[
        create_navbar(),
        html.Div(
            className="container mx-auto px-4 py-8",
            children=[
                html.Div(
                    className="text-center mb-8",
                    children=[
                        html.H1(
                            className="text-4xl font-bold text-green-600",
                            children=[
                                html.I(className="fas fa-book-open mr-3 text-blue-600"),
                                "Islamic Library Collection"
                            ]
                        )
                    ]
                ),

                # Search and Filter Section
                html.Div(
                    className="flex justify-center mb-8",
                    children=[
                        html.Div(
                            className="form-control w-full max-w-xs mr-4",
                            children=[
                                html.Label(
                                    className="label",
                                    children=html.Span(
                                        className="label-text text-green-600",
                                        children="Search Books"
                                    )
                                ),
                                dcc.Input(
                                    id="search-input",
                                    type="text",
                                    placeholder="Search...",
                                    className="input input-bordered border-green-500 w-full max-w-xs"
                                )
                            ]
                        ),
                        html.Div(
                            className="form-control w-full max-w-xs",
                            children=[
                                html.Label(
                                    className="label",
                                    children=html.Span(
                                        className="label-text text-blue-600",
                                        children="Select Category"
                                    )
                                ),
                                dcc.Dropdown(
                                    id="category-select",
                                    options=[
                                        {"label": "All Categories", "value": "All"},
                                        {"label": "Holy Book", "value": "Holy Book"},
                                        {"label": "Hadith", "value": "Hadith"},
                                        {"label": "Islamic Teachings", "value": "Islamic Teachings"}
                                    ],
                                    placeholder="Select Category",
                                    className="w-full max-w-xs"
                                )
                            ]
                        )
                    ]
                ),

                # Books Grid
                html.Div(
                    id="books-grid",
                    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center"
                )
            ]
        )
    ] )

# Callback for Dynamic Book Filtering
@app.callback(
    Output("books-grid", "children"),
    [Input("search-input", "value"),
     Input("category-select", "value")]
)
def update_book_grid(search_term, category):
    filtered_books = df_books.copy()

    # Filter by search term
    if search_term:
        filtered_books = filtered_books[
            filtered_books['title'].str.contains(search_term, case=False) |
            filtered_books['author'].str.contains(search_term, case=False)
        ]

    # Filter by category
    if category and category != "All":
        filtered_books = filtered_books[filtered_books['category'] == category]

    # Create book cards
    book_cards = [
        create_book_card(book.to_dict())
        for _, book in filtered_books.iterrows()
    ]

    return book_cards

# Server configuration
if __name__ == '__main__':
    app.run_server(debug=True)
