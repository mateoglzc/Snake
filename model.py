import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class SnakeLinearQ(nn.Module):

    def __init__(self, input_size, hidden_size, output_size) -> None:
        super(SnakeLinearQ, self).__init__()

        self.linear1 = nn.Linear(
            input_size, 
            hidden_size
        )

        self.relu = nn.ReLU()

        self.linear2 = nn.Linear(
            hidden_size,
            output_size
        )

        
    def forward(self, x):
        
        out = self.linear1(x)
        out = self.relu(out)
        out = self.linear2(out)

        return out

    def saveModel(self, file_name='model.pth') -> None:
        folder_name = './models'

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_name = os.path.join(folder_name,file_name)
        torch.save(self.state_dict(), file_name)


class SnakeTrainer():
    
    def __init__(self, model, gamma, epsilon, lr=0.5) -> None:
        
        self.gamma = gamma
        self.epsilon = epsilon
        self.learning_rate = lr

        self.model = model
        self.optim = torch.optim.Adam(model.parameters(), lr=self.learning_rate)
        self.loss = nn.MSELoss()

    def trainStep(self, state, action, reward, next_state, done) -> None:
            
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        if len(state.shape) == 1:
            
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            done = (done, )

        # Implementation of the bellman equation

        prediction = self.model(state)

        target = prediction.clone()

        for i in range(len(done)):

            new_state = reward[i]

            if not done[i]:
                new_state = reward[i] + self.gamma * torch.max(self.model(next_state[i]))

            target[i][torch.argmax(action[i]).item()] = new_state # Check this

        self.optim.zero_grad()

        loss = self.loss(target, prediction)

        loss.backward()

        self.optim.step()


                                





        

