import argparse
import model
import predictor

def main():


    parser = argparse.ArgumentParser(description="Parkingson's Disease Modeler and Predictor")

    parser.add_argument('--model', choices = ['modeler', 'predictor'], required=True)
    parser.add_argument('--files', type=str, nargs='+', required=True)
    parser.add_argument('--modelFile', type=str, nargs='+', required=False)
    parser.add_argument('--output', default = './')
    parser.add_argument('--filterList', default = '')
    parser.add_argument('--filterFile', default = '')


    args = parser.parse_args()
    print(args.model)

    if args.model == "modeler":
        model.Model()

    elif args.model == "predictor":
        predictor.Predictor()






if __name__ == "__main__":
    main()