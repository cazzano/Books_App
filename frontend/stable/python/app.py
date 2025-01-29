import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import requests

# Initialize Dash App with CDN stylesheets
app = dash.Dash(__name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
        "https://cdn.jsdelivr.net/npm/daisyui@3.9.4/dist/full.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    ]
)

# Fetch books data from the Flask API
def fetch_books():
    response = requests.get('http://localhost:5000/api/books')
    return pd.DataFrame(response.json())

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
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(book['title'], className='font-bold')),
            dbc.CardBody(
                [
                    html.P(f"Author: {book['author']}", className='text-sm'),
                    html.P(f"Category: {book['category']}", className='text-sm'),
                    html.P(f"Rating: {book['rating']}", className='text-sm'),
                    html.I(className=book['icon'], style={'color': book['text_color']}),
                ],
                style={'backgroundColor': book['bg_color']}
            ),
        ],
        className='m-2'
    )

# App Layout
app.layout = html.Div([
    create_navbar(),
    dcc.Input(id='search-input', type='text', placeholder='Search books...'),
    dcc.Dropdown(id='category-select', options=[
        {'label': 'All Categories', 'value': 'All'},
        {'label': 'Holy Book', 'value': 'Holy Book'},
        {'label': 'Hadith', 'value': 'Hadith'},
        {'label': 'Islamic Teachings', 'value': 'Islamic Teachings'},
    ], value='All'),
    html.Div(id='books-grid', className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center')
])

# Callback for Dynamic Book Filtering
@app.callback(
    Output('books-grid', 'children'),
    [Input('search-input', 'value'),
     Input('category-select', 'value')]
)
def update_book_grid(search_term, category):
    df_books = fetch_books()
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
        create_book_card(book) for _, book in filtered_books.iterrows()
    ]

    return book_cards

if __name__ == '__main__':
    app.run_server(debug=True)  # This line is for local development only
