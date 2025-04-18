# Home Appliance Control System

A Python-based GUI application for controlling and monitoring various home appliances using Tkinter.

## Overview

This application simulates a home automation control panel that allows users to turn various appliances on and off while providing visual feedback through animations. The interface is designed to be intuitive and user-friendly, making it easy to monitor the status of all home appliances at a glance.

## Features

- **Interactive Control Panel**: Simple on/off controls for each appliance
- **Visual Animations**: Each appliance type has a unique animation showing its operational status
  - **Lights**: Glowing light bulb animation
  - **Fans**: Rotating fan blades
  - **Air Conditioner**: Flow of cool air particles moving from left to right
  - **TV**: Changing channels with different content
  - **Speaker**: Sound waves emanating outward
  - **Radio**: Equalizer bars that change with the music
- **Configuration Saving**: Save the state of all appliances between sessions
- **Status Updates**: Real-time feedback displayed in the status bar

## Sections

The application is organized into three main sections:

1. **Lighting Control**:
   - Living Room Light
   - Bedroom Light
   - Kitchen Light

2. **Climate Control**:
   - Living Room Fan
   - Bedroom Fan
   - Air Conditioner

3. **Entertainment**:
   - TV
   - Speaker
   - Radio

## Running the Application

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually included with Python installation)

### Steps to Run
1. Clone or download the repository
2. Navigate to the project directory
3. Run the main script:
   ```
   python home_control.py
   ```

## How It Works

The application uses:
- **Tkinter**: For creating the GUI components and layout
- **Canvas**: For drawing the animations
- **JSON**: For saving and loading appliance states
- **Object-Oriented Design**: A class-based approach for better organization and maintainability

## Usage

1. Click the ON/OFF button for any appliance to toggle its state
2. When an appliance is turned on, its representative animation will appear
3. Click "Save Configuration" to save the current state of all appliances
4. States are automatically loaded when the application starts

## Future Enhancements

Potential improvements for future versions:
- Timers and scheduling for appliances
- Temperature controls for climate devices
- Volume controls for entertainment devices
- Remote control via mobile app or web interface
- Integration with actual smart home devices

## License

This project is open source and available under the MIT License. 