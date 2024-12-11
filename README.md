# Trading Office

This project

- gets historical data from the MetaTrader 5 API, 
- anlyzes the currency pairs - for time or serial dependence,
- places trades - buy, short-sell or sell.

The goal is to mirror an automated office of a short-term (daily, weekly or monthly) forex trader. 

## Dependencies

- MetaTrader 5 API
- Exness broker account
- Python packages for Data Science and Machine Learning 

## Getting Started

1. Clone the repository and `cd` into the project.

```bash
git clone https://github.com/Stevealila/Trade.git
cd Analyze-Currency-Pairs
```

2. Create a virtual environment, depending on your operating system:

   A. Windows

   ```bash
   python -m venv venv
   \venv\Scripts\activate
   ```

   B. Unix system

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install project dependencies

```bash
pip install -r requirements.txt
```

4. Install MetaTrader 5 via your Forex broker e.g Exness in this project.
5. Insert your login credentials in `.env`, shown in the `.env.example` file. 
6. Run the your preferred notebook.

## Contribution

Feel free to contribute by opening issues or creating pull requests. Your feedback and improvements are highly welcomed!

## License

This project is licensed under the [MIT License](LICENSE).

***NOTE**: This project is for educational and research purposes only. Forex trading involves significant risk of loss and is not suitable for all investors. Do not trade with money you cannot afford to lose.*
