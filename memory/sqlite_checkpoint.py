from langgraph.checkpoint.sqlite import SqliteSaver


def build_checkpointer():

    checkpointer = SqliteSaver.from_conn_string(
        "sqlite:///db/checkpoints.db"
    )

    return checkpointer