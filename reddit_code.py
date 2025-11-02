import praw
import os
from dotenv import dotenv_values
import pandas as pd

def download_hot_posts(reddit, subreddit_names, limit=10):
    """
    Download hot posts from specified subreddits.

    Args:
        reddit (praw.Reddit): Authenticated Reddit API instance
        subreddit_names (list): Name of the subreddits to download from
        limit (int): Number of posts to download (default: 10)

    Returns:
        list: List containing hot posts
    """
    # Input validation
    if not subreddit_names or not isinstance(subreddit_names, list):
        raise ValueError("Subreddit names must be a non-empty list")
    for subreddit_name in subreddit_names:
        if not subreddit_name or not isinstance(subreddit_name, str):
            raise ValueError("Subreddit name must be a non-empty string")
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit must be a positive integer")

    try:
        hot_posts = []
        for subreddit_name in subreddit_names:
            # Access the specified subreddit
            subreddit = reddit.subreddit(subreddit_name)

            # Fetch the hot posts
            posts = subreddit.hot(limit=limit)

            # Loop through the posts and write to the CSV file
            print(f"Downloading {limit} hot posts from r/{subreddit_name}...\n")

            post_count = 0
            for post in posts:
                hot_posts.append({
                    'title': post.title if post.title else None,
                    'score': post.score if post.score else None,
                    'upvote_ratio': post.upvote_ratio if post.upvote_ratio else None,
                    'num_comments': post.num_comments if post.num_comments else None,
                    'author': post.author if post.author else None,
                    'subreddit': subreddit_name,
                    'url': post.url if post.url else None,
                    'permalink': post.permalink if post.permalink else None,
                    'created_utc': post.created_utc if post.created_utc else None,
                    'is_self': post.is_self if post.is_self else None,
                    'selftext': post.selftext[:500] if post.selftext else None,
                    'flair': post.link_flair_text if post.link_flair_text else None,
                    'domain': post.domain if post.domain else None
                })
                post_count += 1

            print(f"Successfully downloaded {post_count} posts from {subreddit_name}!")
        return hot_posts

    except praw.exceptions.PRAWException as e:
        print(f"Reddit API error: {e}")
        return False
    except ValueError as e:
        print(f"Input validation error: {e}")
        return False
    except FileNotFoundError as e:
        print(f"File error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def search_posts(reddit, query, subreddit_names, limit=10):
    """
    Download keyword posts from specified subreddits.

    Args:
        reddit (praw.Reddit): Authenticated Reddit API instance
        query (str): Keyword or phrase to search for
        subreddit_names (list): Name of the subreddits to download from
        limit (int): Number of posts to download (default: 10)

    Returns:
        list: List containing keyword posts
    """
    # Input validation
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    if not subreddit_names or not isinstance(subreddit_names, list):
        raise ValueError("Subreddit names must be a non-empty list")
    for subreddit_name in subreddit_names:
        if not subreddit_name or not isinstance(subreddit_name, str):
            raise ValueError("Subreddit name must be a non-empty string")
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit must be a positive integer")

    try:
        keyword_posts = []
        for subreddit_name in subreddit_names:
            # Access the specified subreddit
            subreddit = reddit.subreddit(subreddit_name)

            # Fetch the keyword posts
            posts = subreddit.search(query, limit=limit, sort="relevance")

            # Loop through the posts and write to the CSV file
            print(f"Downloading {limit} keyword posts from r/{subreddit_name}...\n")

            post_count = 0
            for post in posts:
                keyword_posts.append({
                    'title': post.title if post.title else None,
                    'score': post.score if post.score else None,
                    'upvote_ratio': post.upvote_ratio if post.upvote_ratio else None,
                    'num_comments': post.num_comments if post.num_comments else None,
                    'author': post.author if post.author else None,
                    'subreddit': subreddit_name,
                    'url': post.url if post.url else None,
                    'permalink': post.permalink if post.permalink else None,
                    'created_utc': post.created_utc if post.created_utc else None,
                    'is_self': post.is_self if post.is_self else None,
                    'selftext': post.selftext[:500] if post.selftext else None,
                    'flair': post.link_flair_text if post.link_flair_text else None,
                    'domain': post.domain if post.domain else None,
                    'search_query': query
                })
                post_count += 1

            print(f"Successfully downloaded {post_count} posts from {subreddit_name}!")
        return keyword_posts

    except praw.exceptions.PRAWException as e:
        print(f"Reddit API error: {e}")
        return False
    except ValueError as e:
        print(f"Input validation error: {e}")
        return False
    except FileNotFoundError as e:
        print(f"File error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def save_to_csv(all_posts, filename="reddit_data.csv"):
    """
    Process, clean, and save collected Reddit post data to CSV.

    Args:
        all_posts (list): A list where each element is a dictionary containing Reddit post attributes
        filename (str): The name of the CSV file to save the cleaned data to

    Returns:
        pandas.Dataframe: DataFrame containing the cleaned and deduplicated Reddit post data
    """
    if not all_posts:
        print("No posts to save.")
        return None

    # Convert to DataFrame
    df = pd.DataFrame(all_posts)

    # Remove duplicates
    before = len(df)
    df.drop_duplicates(subset="permalink", inplace=True)
    after = len(df)

    print(f"Removed {before - after} duplicate posts.")
    print(f"Saving {after} cleaned posts to '{filename}'...\n")

    # Save to CSV (no index)
    df.to_csv(filename, index=False)
    print(f"Data saved successfully to {filename}")
    return df

if __name__ == "__main__":

    # Define the path to your .env file
    # IMPORTANT: Update this path to the actual location of your reddit.env file
    env_file_path = 'reddit.env'

    # Load environment variables from reddit.env file if it exists
    if os.path.exists(env_file_path):
        config = dotenv_values(env_file_path)
        print(f"Environment variables loaded from {env_file_path}!")
    else:
        config = {}
        print(f"Error: '{env_file_path}' not found. Environment variables not loaded.")
        print("Please ensure the 'reddit.env' file is in the specified path.")

    # Authenticate with Reddit using environment variables
    reddit = praw.Reddit(
        client_id=config.get('REDDIT_CLIENT_ID'),
        client_secret=config.get('REDDIT_CLIENT_SECRET'),
        username=config.get('REDDIT_USERNAME'),
        password=config.get('REDDIT_PASSWORD'),
        user_agent=config.get('REDDIT_USER_AGENT')
    )

    print("Reddit API authenticated successfully!")
    print(f"Connected as: {reddit.user.me()}")

    subreddits = ["MachineLearning", "Artificial", "OpenAI"]

    # Collect both types of data
    hot_posts = download_hot_posts(reddit, subreddits)
    search_results = search_posts(reddit, "GPT-4", subreddits)

    # Combine all collected data
    all_collected = hot_posts + search_results

    # Save to CSV
    final_df = save_to_csv(all_collected, filename="reddit_data.csv")

    # Simple summary
    if final_df is not None:
        print(f"\nFinal dataset shape: {final_df.shape}")
        print(f"Columns: {list(final_df.columns)}")



