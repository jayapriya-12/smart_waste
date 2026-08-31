import os

def predict_waste(image_path):

    filename = os.path.basename(image_path).lower()

    if "plastic" in filename:
        return "Plastic Waste", "Recycle in the Blue Recycling Bin."

    elif "paper" in filename:
        return "Paper Waste", "Recycle paper in the Dry Waste Bin."

    elif "glass" in filename:
        return "Glass Waste", "Glass can be recycled multiple times."

    elif "metal" in filename:
        return "Metal Waste", "Recycle metal separately."

    elif "organic" in filename or "banana" in filename or "food" in filename:
        return "Organic Waste", "Use this waste for composting."

    else:
        return "Unknown Waste", "AI model is not trained yet."