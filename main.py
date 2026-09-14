import streamlit as st
import pandas as pd


# =====================================
# PAGE TITLE
# =====================================

st.title("Auto Machine Learning Framework")
st.write("Upload your CSV file to analyze and clean the data.")


# =====================================
# CSV FILE UPLOAD
# =====================================

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


if uploaded_file is not None:

    # Create dataframe only once
    if "df" not in st.session_state:

        st.session_state.df = pd.read_csv(uploaded_file)

    df = st.session_state.df


    # =====================================
    # STEP 1: DATASET ANALYSIS
    # =====================================

    st.header("Step 1: Dataset Analysis")

    st.write("Dataset First 5 Rows:")
    st.dataframe(df.head())

    st.write("Dataset Last 5 Rows:")
    st.dataframe(df.tail())

    st.write("Dataset Shape:")
    st.write(df.shape)

    st.write("Basic Statistics:")
    st.write(df.describe())

    st.write("Column Names:")
    st.write(df.columns.tolist())

    st.write("Data Types:")
    st.write(df.dtypes)


    # =====================================
    # STEP 2: DATA CLEANING
    # =====================================

    st.header("Step 2: Data Cleaning")


    # =====================================
    # 1. MISSING VALUES
    # =====================================

    if "missing_completed" not in st.session_state:

        st.subheader("1. Missing Values")

        action = st.radio(
            "What do you want to do?",
            ["See Missing Values", "Handle Missing Values"]
        )


        # ---------------------------------
        # SEE MISSING VALUES
        # ---------------------------------

        if action == "See Missing Values":

            st.write("Missing Values:")
            st.write(df.isnull().sum())


        # ---------------------------------
        # HANDLE MISSING VALUES
        # ---------------------------------

        if action == "Handle Missing Values":

            st.write(
                "Click the button below to handle the missing values."
            )

            handle_button = st.button("Handle Missing Values")


            if handle_button:

                for column in df.columns:

                    # Check if column has missing values
                    if df[column].isnull().sum() > 0:

                        # Numeric column
                        if df[column].dtype != "object":

                            df[column] = df[column].fillna(
                                df[column].median()
                            )

                        # Text column
                        else:

                            df[column] = df[column].fillna(
                                df[column].mode()[0]
                            )


                # Save cleaned dataframe
                st.session_state.df = df

                # Mark missing values as handled
                st.session_state.missing_handled = True

                st.success(
                    "Missing values handled successfully!"
                )


            # ---------------------------------
            # CHECK MISSING VALUES AGAIN
            # ---------------------------------

            if "missing_handled" in st.session_state:

                st.write(
                    "Now check the missing values again."
                )

                check_button = st.button(
                    "See Missing Values Again"
                )


                if check_button:

                    st.write("Missing Values:")

                    st.write(df.isnull().sum())


                    # Check total missing values
                    total_missing = df.isnull().sum().sum()


                    if total_missing == 0:

                        st.success(
                            "No missing values found!"
                        )

                        # Missing step completed
                        st.session_state.missing_completed = True


    # =====================================
    # 2. DUPLICATED VALUES
    # =====================================

    if "missing_completed" in st.session_state:

        st.subheader("2. Duplicated Values")

        action = st.radio(
            "What do you want to do?",
            [
                "See Duplicated Values",
                "Handle Duplicated Values"
            ]
        )


        # ---------------------------------
        # SEE DUPLICATED VALUES
        # ---------------------------------

        if action == "See Duplicated Values":

            st.write("Duplicated Rows:")

            st.write(
                df.duplicated().sum()
            )


        # ---------------------------------
        # HANDLE DUPLICATED VALUES
        # ---------------------------------

        if action == "Handle Duplicated Values":

            st.write(
                "Click the button below to handle "
                "the duplicated values."
            )

            handle_duplicate = st.button(
                "Handle Duplicated Values"
            )


            if handle_duplicate:

                # Remove duplicate rows
                df = df.drop_duplicates()

                # Save cleaned dataframe
                st.session_state.df = df

                # Mark duplicate handling as completed
                st.session_state.duplicate_handled = True

                st.success(
                    "Duplicated values handled successfully!"
                )


            # ---------------------------------
            # CHECK DUPLICATES AGAIN
            # ---------------------------------

            if "duplicate_handled" in st.session_state:

                st.write(
                    "Now check the duplicated values again."
                )

                check_duplicate = st.button(
                    "See Duplicated Values Again"
                )


                if check_duplicate:

                    st.write("Duplicated Rows:")

                    st.write(
                        df.duplicated().sum()
                    )


                    # Check duplicate count
                    if df.duplicated().sum() == 0:

                        st.success(
                            "No duplicated rows found!"
                        )

                        st.session_state.duplicate_completed = True