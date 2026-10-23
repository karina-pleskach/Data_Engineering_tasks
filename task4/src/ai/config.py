import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = 'openai/gpt-oss-120b'

TABLE_DESCRIPTIONS = """
    books: Contains information about books.
    - id: Unique identifier of a book.
    - title: Title of the book.
    - author: A string containing author names separated by commas. Do not use this column for author-related queries. Use author_set instead.
    - author_set: A set of authors associated with the book. Treat each unique author set as a single author for query purposes. If the user asks to find or count an author, interpret this as finding or counting a unique author set. Do not split the set into individual authors.
    - number_of_authors: Number of authors associated with the book.
    - genre: Literary genre of the book. List of unique genres in the table : ['Western', 'Textbook', 'Biography/Autobiography', 'Narrative nonfiction', 'Tall tale', 'Fantasy', 'Fairy tale', 'Short story', 'Mythopoeia', 'Legend', 'Fanfiction', 'Horror', 'Humor', 'Fiction narrative', 'Crime/Detective', 'Classic', 'Realistic fiction', 'Mythology', 'Folklore', 'Speech', 'Essay', 'Comic/Graphic Novel', 'Mystery', 'Science fiction', 'Historical fiction', 'Suspense/Thriller', 'Metafiction', 'Fiction in verse', 'Fable', 'Reference book']
    - publisher: Publisher of the book.
    - year: Publication year of the book.

    users: Contains user account records. A customer may have multiple user IDs because this table preserves the history of changes to customer accounts.
    - id: Unique identifier of a user account record. It is not a unique identifier of a customer.
    - name: Customer name recorded in the account.
    - address: Customer address recorded in the account.
    - phone: Customer phone number recorded in the account.
    - email: Customer email address recorded in the account.
    - customer_id: Unique identifier of the customer across account records.

    orders: Contains purchase records.
    - id: Unique identifier of an order record.
    - user_id: Identifier of the user account associated with the order. Multiple user IDs may belong to the same customer.
    - book_id: Identifier of the purchased book; references books.id.
    - quantity: Number of copies purchased.
    - unit_price: Price per copy.
    - timestamp: Timestamp of the order.
    - shipping: Shipping cost.
    - paid_price: Total amount paid for the order.
    - date: Order date.
    - customer_id: Unique identifier of the customer who placed the order.

    Important rules:
    - Always use customer_id to identify, count, group, or compare customers. Never treat user_id or users.id as a unique customer identifier.
    - A single customer_id may be associated with multiple user_id values due to account history.
    - When joining tables or analyzing customer behavior, use customer_id to identify the customer whenever possible.
    - For author-related queries, use author_set and treat each author set as one author. Never use the author string column or split it into individual authors.
    - Use only the available tables and columns listed above. Never invent columns, relationships, or results.
"""

QUERY_TOOL = {
    "type": "function",
    "function": {
        "name": "query",
        "description": """
            Execute a query against store data using the Python query() function.

            You MUST follow the exact schema below. Do not use SQL syntax.
            Do not invent parameters or use alternative key names.

            The argvs has these fields:

            1. from: required string. Name of the initial table.
            Use only available tables.

            2. joins: optional array. Each item:
            {
                "table": "table_name",
                "left_on": "column_in_current_dataframe",
                "right_on": "column_in_joined_table",
                "how": "inner" | "left" | "right" | "outer"
            }
            Each join is applied sequentially.
            In case when both table have the same named colums, to the right one _table_name suffix will be added. 
            Be aware of it for future references.

            3. where: optional filter expression.
            A single condition:
            {
                "column": "column_name",
                "operator": "eq" | "ne" | "gt" | "lt" |
                            "gte" | "lte" | "in" |
                            "contains" | "starts_with" | "regex" |
                            "ends_with" | "is_null" | "is_not_null",
                "value": "comparison value"
            }
            The value field is omitted for is_null and is_not_null.
            For in, value must be an array.
            For literal string matching, use contains, starts_with or ends_with.
            For regex patterns, use regex.
            For equality, use eq, NEVER "=" or "==".
            For inequality, use ne.
            For greater than, use gt.
            For less than, use lt.
            For greater than or equal, use gte.
            For less than or equal, use lte.

            Multiple conditions:
            {
                "logic": "and" | "or",
                "conditions": [condition, condition]
            }
            Conditions may contain nested groups.

            4. group_by: optional string or array of column names.
            Use this to group rows before aggregation.

            5. aggregations: optional array. Each item:
            {
                "column": "column_name",
                "function": "sum" | "mean" | "min" | "max" |
                            "count" | "nunique" | "first" | "last",
                "as": "output_column_name"
            }
            Every aggregation MUST include column, function, and as.
            Every aggregation must include "as", which names the output column.
            Use that exact output name in having and sort.
            Do not use a separate select field.

            6. having: optional filter expression.
            Same structure as where. Applied after aggregation.
            Refer to output column names when filtering aggregated results.

            7. distinct: optional boolean or array of column names.
            true removes duplicate rows; an array specifies columns
            used to identify duplicates.

            8. sort: optional array. Each item:
            {
                "column": "column_name",
                "ascending": true | false
            }
            Use ascending=false for descending order.
            Never use order_by or direction.

            9. limit: optional non-negative integer.

            Execution order:
            joins -> where -> group_by and aggregations ->
            having -> distinct -> sort -> limit.

            Rules:
            - Use only columns that exist in the supplied tables or are created
            by an aggregation.
            - Use the query engine to calculate answers. Never calculate totals
            or counts yourself.
            - Choose an aggregation that matches the question.
            - For "how many books", count distinct book IDs using
            function=nunique on column id when counting after joins.
            - For "how many unique publishers/authors", use nunique only
            when the target column represents one value per entity.
            - If the question cannot be answered using the available columns
            and supported operations, explain the limitation instead of guessing.
            - Return a argvs that matches this schema exactly.

            Here is an example of filled argvs:
            argvs = {
                "from": "books",
                "joins": [
                    {
                        "table": "orders",
                        "left_on": "id",
                        "right_on": "book_id",
                        "how": "inner"
                    }
                ],
                "where": {
                    "logic": "and",
                    "conditions": [
                        {
                            "column": "genre",
                            "operator": "eq",
                            "value": "Historical fiction"
                        },      
                        {
                            "logic": "or",
                            "conditions": [
                                {
                                    "column": "year",
                                    "operator": "gte",
                                    "value": 2020
                                },      
                                {
                                    "column": "year",
                                    "operator": "lt",
                                    "value": 2000
                                }
                            ]
                        }
                    ]
                },
                "group_by": "publisher",
                "aggregations": [
                    {
                        "column": "id",
                        "function": "nunique",
                        "as": "book_count"
                    }
                ],
                "having": {
                    "column": "book_count",
                    "operator": "gte",
                    "value": 1
                },
                "distinct": true,
                "sort": [
                    {
                        "column": "publisher",
                        "ascending": false
                    }
                ],
                "limit": 5
            }
            """,
        "parameters": {
            "type": "object",
            "properties": {
                "argvs": {
                    "type": "object",
                    "properties": {
                        "from": {
                            "type": "string",
                            "enum": ["books", "orders", "users"]
                        },
                        "joins": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "table": {
                                        "type": "string",
                                        "enum": ["books", "orders", "users"]
                                    },
                                    "left_on": {"type": "string"},
                                    "right_on": {"type": "string"},
                                    "how": {
                                        "type": "string",
                                        "enum": ["inner", "left", "right", "outer"]
                                    }
                                },
                                "required": [
                                    "table", "left_on", "right_on", "how"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "where": {
                            "anyOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "column": {"type": "string"},
                                        "operator": {
                                            "type": "string",
                                            "enum": [
                                                "eq", "ne", "gt", "lt",
                                                "gte", "lte", "in",
                                                "contains", "starts_with",
                                                "ends_with", "regex",
                                                "is_null", "is_not_null"
                                            ]
                                        },
                                        "value": {}
                                    },
                                    "required": ["column", "operator"],
                                    "additionalProperties": False
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "logic": {
                                            "type": "string",
                                            "enum": ["and", "or"]
                                        },
                                        "conditions": {
                                            "type": "array",
                                            "items": {"type": "object"}
                                        }
                                    },
                                    "required": ["logic", "conditions"],
                                    "additionalProperties": False
                                }
                            ]
                        },
                        "group_by": {
                            "anyOf": [
                                {"type": "string"},
                                {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                {"type": "null"}
                            ]
                        },
                        "aggregations": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "column": {"type": "string"},
                                    "function": {
                                        "type": "string",
                                        "enum": [
                                            "sum", "mean", "min", "max",
                                            "count", "nunique", "first", "last"
                                        ]
                                    },
                                    "as": {"type": "string"}
                                },
                                "required": ["column", "function", "as"],
                                "additionalProperties": False
                            }
                        },
                        "having": {
                            "type": ["object", "null"]
                        },
                        "distinct": {
                            "anyOf": [
                                {"type": "boolean"},
                                {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                {"type": "null"}
                            ]
                        },
                        "sort": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "column": {"type": "string"},
                                    "ascending": {"type": "boolean"}
                                },
                                "required": ["column", "ascending"],
                                "additionalProperties": False
                            }
                        },
                        "limit": {
                            "type": ["integer", "null"]
                        }
                    },
                    "required": ["from"],
                    "additionalProperties": False
                }
            },
            "required": ["argvs"],
            "additionalProperties": False
        }
    }
}