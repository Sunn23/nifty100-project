import pandas as pd

def save_validation_report(failures, output_file):

    df = pd.DataFrame(failures)

    df.to_csv(output_file, index=False)

    print(f"Validation report saved to {output_file}")