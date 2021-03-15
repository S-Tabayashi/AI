import numpy as np


class SplitData(object):
    def __init__(self, df):
        # 2次元データを生成
        self.split_data = np.array(df)
        self.add_position = 0
        self.record_count = 1

    def add_data(self, df):

        if self.record_count == 1:
            # 生成後に３次元方向にデータを追加する
            if len(self.split_data.shape) == 1 & len(df.shape) == 1:
                # 1次元データに1次元データを追加する場合はパディングしない
                add_data = np.array(df)
            elif self.split_data.shape[0] >= df.shape[0]:
                # 追加するデータのシェイプが小さい場合は、max_shapeに合わせる
                add_data = np.pad(np.array(df),
                                  [(self.split_data.shape[0]
                                    - df.shape[0], 0),
                                   (0, 0)],'constant')
            else:
                # 追加するデータのシェイプが大きい場合は、追加するデータにshapeに合わせてから
                # データを追加する
                add_data = np.array(df)
                self.split_data = np.pad(self.split_data,
                                         [(df.shape[0]
                                           - self.split_data.shape[0], 0),
                                          (0, 0)], 'constant')
            self.split_data = np.stack([self.split_data, add_data])
            self.record_count += 1

        else:
            # 3次元のデータに3次元方向に追加する
            current_position = self.get_current_position()
            add_position = self.get_add_position()

            if self.split_data[current_position].shape[0] >= df.shape[0]:
                add_axis = (self.split_data[current_position].shape[0]
                            - df.shape[0], 0)

                # 追加するデータのシェイプが小さい場合は、max_shapeに合わせてパディングする
                if len(df.shape) == 1:
                    add_data = np.pad(np.array(df),
                                      [add_axis], 'constant')
                else:
                    add_data = np.pad(np.array(df),
                                      [add_axis, (0, 0)], 'constant')
            else:
                add_data = np.array(df)
                # 追加するデータのシェイプが大きい場合は、生成済みのデータをパディングする
                add_axis = (df.shape[0] - self.split_data[current_position].
                            shape[0], 0)

                if len(df.shape) == 1:
                    self.split_data = np.pad(self.split_data,
                                             [(0, 0), add_axis],
                                             'constant')
                else:
                    self.split_data = np.pad(self.split_data,
                                             [(0, 0), add_axis, (0, 0)],
                                             'constant')

            self.split_data = np.insert(self.split_data, add_position,
                                        add_data, axis=0)
            self.record_count += 1

    def get_current_position(self):
        return self.record_count - 1

    def get_add_position(self):
        return self.record_count

    def get_data(self):
        return self.split_data

