import pandas as pd
import numpy as np

def data_competition_evaluation(phase="Phase 2", name=""):

    # Submission should be loaded from a .csv file.    
    submission = pd.read_csv(name)
    assert all(col in submission.columns for col in ["Client", "Warehouse", "Product"])
    submission = submission.set_index(["Client", "Warehouse", "Product"])
    submission.columns = pd.to_datetime(submission.columns)
    assert (~submission.isnull().any().any())

    # Load Objective
    objective = pd.read_csv(f"{phase} - Sales.csv").set_index(["Client", "Warehouse", "Product"])
    objective.columns = pd.to_datetime(objective.columns)
    assert (submission.index == objective.index).all()
    assert (submission.columns == objective.columns).all()
    
    # This is an important rule that we communicate to competitors.
    abs_err = np.nansum(abs(submission - objective))
    err = np.nansum((submission - objective))
    score = abs_err + abs(err)
    score /= objective.sum().sum()
    print(f"{name}:", score) #It's a percentage
    

def data_competition_dummy_submission_phase1():
    
    data = pd.read_csv("Phase 0 - Sales.csv").set_index(["Client", "Warehouse", "Product"])
    data.columns = pd.to_datetime(data.columns)
    data.sum().plot()
    
    # Create a random sumission
    name = "Submission Phase 1 - Random.csv"
    submission = pd.DataFrame(
                    index = data.index,
                    columns = pd.date_range(start=data.columns.max(), periods=14, freq="W-MON", inclusive="neither"),
                    data = np.random.randint(low=0, high=20, size=(data.shape[0], 13))
                    )   
    submission.to_csv(name)
    data_competition_evaluation(phase="Phase 1", name=name)

    # MA12
    name = "Submission Phase 1 - MA12.csv"
    submission = pd.DataFrame(
        index = data.index,
        columns = pd.date_range(start=data.columns.max(), periods=14, freq="W-MON", inclusive="neither"),
        data = np.repeat(np.nanmean(data.values[:,-12:], axis=1).reshape(-1,1), 13, axis=1)
        )
    submission.to_csv(name)
    data_competition_evaluation(phase="Phase 1", name=name)


def data_competition_dummy_submission_phase2():
    
    data = pd.concat([pd.read_csv("Phase 0 - Sales.csv").set_index(["Client", "Warehouse", "Product"]),
                      pd.read_csv("Phase 1 - Sales.csv").set_index(["Client", "Warehouse", "Product"]),], axis=1)                    
    data.columns = pd.to_datetime(data.columns)
    data.sum().plot()
    
    # Create a random sumission
    name = "Submission Phase 2 - Random.csv"
    submission = pd.DataFrame(
                    index = data.index,
                    columns = pd.date_range(start=data.columns.max(), periods=14, freq="W-MON", inclusive="neither"),
                    data = np.random.randint(low=0, high=20, size=(data.shape[0], 13))
                    )   
    submission.to_csv(name)
    data_competition_evaluation(phase="Phase 2", name=name)

    # MA12
    name = "Submission Phase 2 - MA12.csv"
    submission = pd.DataFrame(
        index = data.index,
        columns = pd.date_range(start=data.columns.max(), periods=14, freq="W-MON", inclusive="neither"),
        data = np.repeat(np.nanmean(data.values[:,-12:], axis=1).reshape(-1,1), 13, axis=1)
        )
    submission.to_csv(name)
    data_competition_evaluation(phase="Phase 2", name=name)


data_competition_dummy_submission_phase1()
data_competition_dummy_submission_phase2()
