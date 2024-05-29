import pandas as pd
import subprocess
from pathlib import Path

def process_data(input_file_path, data_3DPoints, data_Lengths):
    data = pd.read_csv(input_file_path, delim_whitespace=True)

    processed_rows = []
    skip_next = False
    for i in range(len(data)):
        if skip_next:
            skip_next = False
            continue

        if i == len(data) - 1:
            processed_rows.append(data.iloc[i][['OpCode', 'ImagePtPair', 'Lx', 'Ly', 'Rx', 'Ry']].tolist())
        else:
            current_row = data.iloc[i]
            next_row = data.iloc[i + 1]

            if current_row['ImagePtPair'] == next_row['ImagePtPair']:
                mean_row = current_row[['Lx', 'Ly', 'Rx', 'Ry']].add(next_row[['Lx', 'Ly', 'Rx', 'Ry']]).div(2)
                processed_rows.append([current_row['OpCode'], current_row['ImagePtPair'] , mean_row[['Lx', 'Ly', 'Rx', 'Ry']].tolist()[0],mean_row[['Lx', 'Ly', 'Rx', 'Ry']].tolist()[1], mean_row[['Lx', 'Ly', 'Rx', 'Ry']].tolist()[2], mean_row[['Lx', 'Ly', 'Rx', 'Ry']].tolist()[3]])
                skip_next = True
            else:
                processed_rows.append(current_row[['OpCode', 'ImagePtPair', 'Lx', 'Ly', 'Rx', 'Ry']].tolist())

    processed_data = pd.DataFrame(processed_rows, columns=['OpCode', 'ImagePtPair', 'Lx', 'Ly', 'Rx', 'Ry'])
    columns_to_add = ['FilenameLeft', 'FrameLeft', 'FilenameRight', 'FrameRight', 'Time', 'Code', 'Number'] 

    for col in columns_to_add:
        processed_data[col] = pd.NA

    # Loop through each row and find corresponding data in 3DPoints and Lengths
    for i, row in processed_data.iterrows():

        # Search for a matching row in data_3DPoints
        match_3DPoints = data_3DPoints[(data_3DPoints['ImagePtPair'] == row['ImagePtPair']) & (data_3DPoints['OpCode'] == row['OpCode'])]
        if not match_3DPoints.empty:
            for col in match_3DPoints.columns:
                if col in columns_to_add:
                    processed_data.at[i, col] = match_3DPoints.iloc[0][col]

        # Search for a matching row in data_Lengths
        match_Lengths = data_Lengths[(data_Lengths['ImagePtPair'] == row['ImagePtPair']) & (data_Lengths['OpCode'] == row['OpCode'])]
        if not match_Lengths.empty:
            for col in match_Lengths.columns:
                if col in columns_to_add:
                    processed_data.at[i, col] = match_Lengths.iloc[0][col]

        if pd.notna(processed_data.at[i, 'FilenameLeft']):
            processed_data.at[i, 'FilenameLeft'] = processed_data.at[i, 'FilenameLeft'].replace('.MP4', '')

        if pd.notna(processed_data.at[i, 'FilenameRight']):
            processed_data.at[i, 'FilenameRight'] = processed_data.at[i, 'FilenameRight'].replace('.MP4', '')

    return processed_data





def process_video_frames(df, side, videos_base_dir, output_frames_dir, frame_rate):
    points_dict = {}
    images_path = []
    
    for i, row in df.iterrows():
        base_filename = row['FilenameLeft'] if side == 'Left' else row['FilenameRight']
        base_filename = base_filename.split('.')[0]  # Remove the .MP4 extension if present
        video_path = Path(videos_base_dir) / row['OpCode'] / 'videos' / f"{base_filename}.MP4"
        frame_number = row['FrameLeft'] if side == 'Left' else row['FrameRight']

        if pd.isna(row['Code']):
            species_code = 0000  # Default code
        else:
            species_code = int(row['Code'])

        coords = [row['Lx'], row['Ly']] if side == 'Left' else [row['Rx'], row['Ry']]
        
        output_image_path = Path(output_frames_dir) / f"{row['OpCode']}_{base_filename}_{frame_number}_{species_code}.png"
        
        if not video_path.exists():
            print(f'Video file not found: {video_path}')
            continue
        
        if output_image_path in points_dict:
            points_dict[output_image_path].append(coords)
        else:
            points_dict[output_image_path] = [coords]
        images_path.append(output_image_path)
        print(output_image_path)
        
        if not output_image_path.exists():
            subprocess.run([
                'ffmpeg', '-y', '-loglevel', 'panic', '-i', str(video_path), 
                '-vf', f'select=gte(n\,{frame_number})', '-vframes', '1',
                '-frames:v', '1', str(output_image_path)
            ], check=True)
    
    return points_dict, images_path

