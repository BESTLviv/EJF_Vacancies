from typing import Iterator

class Vacancy:

    pass




    def add_vacancy(self):
        add_vacancy_steps = [
            self.input_name, 
            self.input_category,
            self.input_experience, 
            self.input_work_type,
            self.input_description,
            self.finish_add_vacancy]

        steps_iterator = iter(add_vacancy_steps)



    def input_name(self, next_step:Iterator=None):
        pass

    def _process_input_name(self, message, **kwargs):
        next_step = kwargs["next_step"]


        if next(next_step, None) is not None:
            next_step(next_step)



    def input_category(self, next_step:Iterator=None):
        pass

    def _process_input_category(self, message, **kwargs):
        next_step = kwargs["next_step"]


        if next(next_step, None) is not None:
            next_step(next_step)




    def input_experience(self, next_step:Iterator=None):
        pass

    def _process_input_experience(self, message, **kwargs):
        next_step = kwargs["next_step"]


        if next(next_step, None) is not None:
            next_step(next_step)




    def input_work_type(self, next_step:Iterator=None):
        pass

    def _process_input_work_type(self, message, **kwargs):
        next_step = kwargs["next_step"]


        if next(next_step, None) is not None:
            next_step(next_step)




    def input_description(self, next_step:Iterator=None):
        pass

    def _process_input_description(self, message, **kwargs):
        next_step = kwargs["next_step"]


        if next(next_step, None) is not None:
            next_step(next_step)




    def finish_add_vacancy(self, next_step:Iterator=None):
        pass

