# Chat with BEA API

Example of how to chat with an API

This procedure assumes you have obtained your API key by registering at the BEA website.

### Functional Testing Procedure

#### 1. Testing with the "NIPA" Dataset

- **Dataset Name**: NIPA (National Income and Product Accounts)
- **Parameter Key**: TableName
- **Parameter Value**: One of the specific table names for NIPA data. Use "T10101" for Gross Domestic Product.
- **Additional Parameters**: You can specify `Frequency` and `Year` as additional parameters.
  - **Frequency**: A (Annual)
  - **Year**: 2020

**Procedure**:
- Enter the BEA API key when prompted.
- For the dataset name, enter `NIPA`.
- When prompted for the parameter key, enter `TableName`, and for its value, enter `T10101`.
- To add more parameters, specify `Frequency` as the next parameter key and `A` as its value for annual data.
- Finally, add `Year` as a parameter key and `2020` as its value.
- Review the output for GDP data for the year 2020.

#### 2. Testing with the "Regional" Dataset

- **Dataset Name**: Regional
- **Parameter Key 1**: GeoFIPS
- **Parameter Value 1**: `STATE` (for all states)
- **Parameter Key 2**: TableName
- **Parameter Value 2**: `CAINC1` (Personal Income Summary)
- **Parameter Key 3**: Year
- **Parameter Value 3**: 2019

**Procedure**:
- Start the script again and enter your API key.
- For the dataset name, enter `Regional`.
- For the first parameter key, enter `GeoFIPS`, and its value should be `STATE`.
- Next, enter `TableName` as the parameter key and `CAINC1` for the value to query the Personal Income Summary.
- Add `Year` as another parameter key and set its value to `2019`.
- Observe the output, which should display personal income summaries for all states for the year 2019.

#### 3. General Testing Tips

- **Experiment with Different Parameters**: The BEA API documentation provides a comprehensive list of datasets, tables, and parameters. Experiment with different combinations to understand how the API responds and to ensure your application handles various data structures correctly.
- **Check for Error Handling**: Intentionally input incorrect or invalid parameters to see if the application provides helpful error messages. For example, use an invalid dataset name or year to see how the app behaves.
- **Validate Data Accuracy**: For a few test cases, cross-reference the output of your application with the data available on the BEA website to ensure accuracy.
- **Performance Testing**: If you plan to make multiple or complex queries, observe the app's performance, including response times and handling of large data sets.

### Final Note

This structured approach will help you validate the functionality and robustness of your application across different use cases. As you test, you might find areas for improvement or expansion, such as adding more descriptive prompts, improving the parsing of complex data structures, or enhancing error messages for a better user experience.
