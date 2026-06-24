import pandas as pd
from datetime import datetime

def create_audit_log(audit_records, output_file):

    df = pd.DataFrame(audit_records)

    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df.to_csv(output_file, index=False)

    print(f"\nAudit log saved to {output_file}")